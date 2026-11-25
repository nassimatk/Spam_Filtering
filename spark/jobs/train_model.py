"""
Propriétaire : E3
Entraînement et évaluation du modèle de détection Spam avec Spark MLlib.
"""

import argparse
from datetime import datetime, timezone

from pyspark.sql import functions as F
from pyspark.ml import Pipeline, PipelineModel
from pyspark.ml.classification import NaiveBayes

from lakehouse.spark_conf import get_spark
from lakehouse import config
from features import clean_text, build_feature_pipeline


def parse_args():
    parser = argparse.ArgumentParser(description="Entraîner le modèle Spam")

    parser.add_argument(
        "--data",
        default="/opt/app/data/processed/train.jsonl",
        help="Chemin du fichier JSONL d'entraînement",
    )
    parser.add_argument(
        "--model-output",
        default=None,
        help="Chemin de sauvegarde du modèle",
    )
    parser.add_argument(
        "--test-ratio",
        type=float,
        default=0.20,
        help="Proportion des données réservée au test",
    )
    parser.add_argument(
        "--seed",
        type=int,
        default=42,
        help="Graine aléatoire",
    )

    return parser.parse_args()


def main():
    args = parse_args()

    if not 0 < args.test_ratio < 1:
        raise ValueError("test-ratio doit être compris entre 0 et 1.")

    spark = get_spark("Spam-Model-Training")

    try:
        print("1. Chargement des données...")

        df = spark.read.json(args.data)

        required_columns = {"body", "label"}
        missing = required_columns - set(df.columns)

        if missing:
            raise ValueError(f"Colonnes manquantes : {missing}")

        # Nettoyage du texte et normalisation des étiquettes
        df = clean_text(df)

        df = df.withColumn(
            "label_normalized",
            F.lower(F.trim(F.col("label")))
        )

        # Seules les classes ham et spam sont acceptées
        df = df.filter(
            F.col("label_normalized").isin("ham", "spam")
        )

        df = df.withColumn(
            "label_index",
            F.when(F.col("label_normalized") == "spam", 1.0)
             .otherwise(0.0)
        )

        total = df.count()

        if total < 10:
            raise ValueError(
                f"Données insuffisantes pour entraîner le modèle : {total}"
            )

        print(f"Nombre de messages valides : {total}")
        df.groupBy("label_normalized").count().show()

        print("2. Séparation entraînement / test...")

        train_df, test_df = df.randomSplit(
            [1.0 - args.test_ratio, args.test_ratio],
            seed=args.seed,
        )

        train_count = train_df.count()
        test_count = test_df.count()

        if train_count == 0 or test_count == 0:
            raise ValueError("La séparation train/test est impossible.")

        print(f"Entraînement : {train_count}")
        print(f"Test : {test_count}")

        print("3. Construction du pipeline TF-IDF + Naive Bayes...")

        feature_pipeline = build_feature_pipeline()

        classifier = NaiveBayes(
            labelCol="label_index",
            featuresCol="features",
            predictionCol="prediction",
            probabilityCol="probability",
            modelType="multinomial",
        )

        pipeline = Pipeline(
            stages=feature_pipeline.getStages() + [classifier]
        )

        print("4. Entraînement du modèle...")

        model = pipeline.fit(train_df)

        print("5. Évaluation sur les données de test...")

        predictions = model.transform(test_df)

        # Calcul des vrais positifs, faux positifs et faux négatifs
        counts = predictions.agg(
            F.sum(
                F.when(
                    (F.col("label_index") == 1.0)
                    & (F.col("prediction") == 1.0), 1
                ).otherwise(0)
            ).alias("tp"),
            F.sum(
                F.when(
                    (F.col("label_index") == 0.0)
                    & (F.col("prediction") == 1.0), 1
                ).otherwise(0)
            ).alias("fp"),
            F.sum(
                F.when(
                    (F.col("label_index") == 1.0)
                    & (F.col("prediction") == 0.0), 1
                ).otherwise(0)
            ).alias("fn"),
            F.sum(
                F.when(
                    F.col("label_index") == F.col("prediction"), 1
                ).otherwise(0)
            ).alias("correct"),
        ).first()

        tp = int(counts["tp"] or 0)
        fp = int(counts["fp"] or 0)
        fn = int(counts["fn"] or 0)
        correct = int(counts["correct"] or 0)

        accuracy = correct / test_count
        precision = tp / (tp + fp) if tp + fp else 0.0
        recall = tp / (tp + fn) if tp + fn else 0.0
        f1 = (
            2 * precision * recall / (precision + recall)
            if precision + recall else 0.0
        )

        print("\n========== RÉSULTATS DU MODÈLE ==========")
        print(f"Accuracy       : {accuracy:.4f}")
        print(f"Precision spam : {precision:.4f}")
        print(f"Recall spam    : {recall:.4f}")
        print(f"F1-score spam  : {f1:.4f}")
        print(f"TP={tp} | FP={fp} | FN={fn}")
        print("=========================================\n")

        print("Matrice de confusion :")
        predictions.groupBy(
            "label_index", "prediction"
        ).count().orderBy(
            "label_index", "prediction"
        ).show()

        # Sauvegarde du modèle complet : TF-IDF + Naive Bayes
        version = datetime.now(timezone.utc).strftime("%Y%m%d%H%M%S")

        output_path = args.model_output or config.s3a(
            "models", "spam", f"{version}-naive-bayes"
        )

        print(f"6. Sauvegarde du modèle : {output_path}")

        model.write().overwrite().save(output_path)

        print("Modèle sauvegardé avec succès.")

    finally:
        spark.stop()


if __name__ == "__main__":
    main()
