"""Propriétaire : E2 — get_spark() : SparkSession configurée pour MinIO (S3A) et Hudi

Utilisation dans un job :
    from lakehouse.spark_conf import get_spark
    spark = get_spark("stream_bronze")

Les JAR (Hudi bundle, hadoop-aws, aws-java-sdk-bundle, connecteur Kafka) sont normalement installés dans
l'image Spark (spark/Dockerfile, E3). Pour un essai sans image préparée, définir la variable d'environnement
SPARK_JARS_PACKAGES avec les coordonnées Maven (voir docs/versions.md) : Spark les télécharge au démarrage.
"""
import os

from pyspark.sql import SparkSession

from lakehouse import config


def get_spark(app_name="il15-spam", master=None, extra_conf=None):
    """Crée (ou récupère) la SparkSession, prête à lire et écrire dans MinIO (S3A) et dans des tables Hudi."""
    access_key, secret_key = config.s3_credentials()

    conf = {
        # --- MinIO via S3A ---------------------------------------------------
        "spark.hadoop.fs.s3a.impl": "org.apache.hadoop.fs.s3a.S3AFileSystem",
        "spark.hadoop.fs.s3a.endpoint": config.S3_ENDPOINT,
        "spark.hadoop.fs.s3a.access.key": access_key,
        "spark.hadoop.fs.s3a.secret.key": secret_key,
        # MinIO exige l'adressage « path-style » (http://minio:9000/bucket/...) et non bucket.minio:9000
        "spark.hadoop.fs.s3a.path.style.access": "true",
        "spark.hadoop.fs.s3a.connection.ssl.enabled": "false",
        "spark.hadoop.fs.s3a.aws.credentials.provider": "org.apache.hadoop.fs.s3a.SimpleAWSCredentialsProvider",
        # --- Hudi --------------------------------------------------------------
        "spark.serializer": "org.apache.spark.serializer.KryoSerializer",
        "spark.sql.extensions": "org.apache.spark.sql.hudi.HoodieSparkSessionExtension",
        "spark.sql.catalog.spark_catalog": "org.apache.spark.sql.hudi.catalog.HoodieCatalog",
        "spark.kryo.registrator": "org.apache.spark.HoodieSparkKryoRegistrar",
    }

    packages = os.environ.get("SPARK_JARS_PACKAGES")
    if packages:
        conf["spark.jars.packages"] = packages
    if extra_conf:
        conf.update(extra_conf)

    builder = SparkSession.builder.appName(app_name)
    if master:
        builder = builder.master(master)
    for key, value in conf.items():
        builder = builder.config(key, value)
    return builder.getOrCreate()
