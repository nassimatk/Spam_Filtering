"""Création de la SparkSession (S3A/MinIO + Hudi) — propriétaire : E2, utilisée par E3.

Le master n'est PAS fixé ici : il est donné par `spark-submit --master spark://spark-master:7077`.
Les JAR (Hudi, hadoop-aws, Kafka, PostgreSQL) sont inclus dans l'image spark/Dockerfile.
"""
from pyspark.sql import SparkSession

from lakehouse import config


def get_spark(app_name, extra_conf=None):
    builder = (
        SparkSession.builder.appName(app_name)
        # --- MinIO via S3A
        .config("spark.hadoop.fs.s3a.endpoint", config.S3_ENDPOINT)
        .config("spark.hadoop.fs.s3a.access.key", config.S3_ACCESS_KEY)
        .config("spark.hadoop.fs.s3a.secret.key", config.S3_SECRET_KEY)
        .config("spark.hadoop.fs.s3a.path.style.access", "true")
        .config("spark.hadoop.fs.s3a.connection.ssl.enabled", "false")
        .config("spark.hadoop.fs.s3a.impl", "org.apache.hadoop.fs.s3a.S3AFileSystem")
        # --- Hudi (Spark 3.4 / Hudi 0.14)
        .config("spark.serializer", "org.apache.spark.serializer.KryoSerializer")
        .config("spark.sql.extensions", "org.apache.spark.sql.hudi.HoodieSparkSessionExtension")
        .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.hudi.catalog.HoodieCatalog")
        .config("spark.kryo.registrator", "org.apache.spark.HoodieSparkKryoRegistrar")
        .config("spark.sql.session.timeZone", "UTC")
        .config("spark.sql.shuffle.partitions", "4")
    )
    for key, value in (extra_conf or {}).items():
        builder = builder.config(key, value)
    spark = builder.getOrCreate()
    spark.sparkContext.setLogLevel("WARN")
    return spark
