"""
Propriétaire : E3
Prétraitement du texte et extraction des caractéristiques pour le modèle Spam.
Utilisé par train_model.py et stream_classify.py.
"""

from pyspark.sql import DataFrame
from pyspark.sql import functions as F
from pyspark.ml import Pipeline
from pyspark.ml.feature import (
    RegexTokenizer,
    StopWordsRemover,
    HashingTF,
    IDF,
)


def clean_text(df: DataFrame) -> DataFrame:
    """
    Nettoie la colonne body sans utiliser label comme caractéristique.
    """
    if "body" not in df.columns:
        raise ValueError("La colonne obligatoire 'body' est absente.")

    return df.withColumn(
        "body",
        F.trim(F.coalesce(F.col("body"), F.lit("")))
    )


def build_feature_pipeline(num_features: int = 262144) -> Pipeline:
    """
    Construit le pipeline NLP : Tokenizer -> StopWords -> TF -> IDF.

    La sortie finale est la colonne 'features', utilisable par MLlib.
    """
    if num_features <= 0:
        raise ValueError("num_features doit être strictement positif.")

    tokenizer = RegexTokenizer(
        inputCol="body",
        outputCol="tokens",
        pattern=r"\W+",
        gaps=True,
        minTokenLength=2,
        toLowercase=True,
    )

    stop_words = StopWordsRemover(
        inputCol="tokens",
        outputCol="filtered_tokens",
    )

    hashing_tf = HashingTF(
        inputCol="filtered_tokens",
        outputCol="raw_features",
        numFeatures=num_features,
    )

    idf = IDF(
        inputCol="raw_features",
        outputCol="features",
    )

    return Pipeline(stages=[
        tokenizer,
        stop_words,
        hashing_tf,
        idf,
    ])
