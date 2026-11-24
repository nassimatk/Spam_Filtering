"""Propriétaire : E2 — Test en deux temps : Spark <-> MinIO (Parquet) puis Spark <-> Hudi sur MinIO.

Lancement (dans le conteneur Spark, une fois l'image d'E3 disponible) :
    spark-submit /opt/lakehouse/smoke_test_s3a.py
Résultat attendu : « TEST OK » et code de sortie 0.
"""
import sys

from lakehouse.config import s3a_path
from lakehouse.spark_conf import get_spark


def test_parquet(spark):
    chemin = s3a_path("bronze", "test")
    df = spark.createDataFrame([(1, "a"), (2, "b")], ["id", "valeur"])
    df.write.mode("overwrite").parquet(chemin)
    relu = spark.read.parquet(chemin)
    assert relu.count() == 2, "Parquet : 2 lignes attendues dans %s" % chemin
    print("[1/2] Parquet S3A OK : %s" % chemin)


def test_hudi(spark):
    chemin = s3a_path("silver", "test_hudi")
    options = {
        "hoodie.table.name": "test_hudi",
        "hoodie.datasource.write.table.type": "COPY_ON_WRITE",
        "hoodie.datasource.write.operation": "upsert",
        "hoodie.datasource.write.recordkey.field": "message_id",
        "hoodie.datasource.write.precombine.field": "ingest_ts",
        "hoodie.datasource.write.partitionpath.field": "event_date",
        "hoodie.datasource.write.hive_style_partitioning": "true",
    }
    df = spark.createDataFrame(
        [("m1", "bonjour", 1, "2026-11-20"), ("m2", "salut", 1, "2026-11-20")],
        ["message_id", "body", "ingest_ts", "event_date"],
    )
    df.write.format("hudi").options(**options).mode("overwrite").save(chemin)
    relu = spark.read.format("hudi").load(chemin)
    assert relu.count() == 2, "Hudi : 2 lignes attendues dans %s" % chemin
    print("[2/2] Table Hudi S3A OK : %s" % chemin)


def main():
    spark = get_spark("smoke_test_s3a")
    test_parquet(spark)
    test_hudi(spark)
    print("TEST OK")
    spark.stop()


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:  # noqa: BLE001
        print("TEST ECHEC : %s" % exc, file=sys.stderr)
        sys.exit(1)
