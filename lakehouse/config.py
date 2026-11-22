"""Configuration commune (lue dans les variables d'environnement définies par docker-compose)."""
import os

S3_ENDPOINT = os.getenv("S3_ENDPOINT", "http://minio:9000")
S3_ACCESS_KEY = os.getenv("S3_ACCESS_KEY", "minioadmin")
S3_SECRET_KEY = os.getenv("S3_SECRET_KEY", "minioadmin123")

KAFKA_BOOTSTRAP = os.getenv("KAFKA_BOOTSTRAP", "kafka:9092")
KAFKA_TOPIC = os.getenv("KAFKA_TOPIC", "messages")

POSTGRES_HOST = os.getenv("POSTGRES_HOST", "postgres")
POSTGRES_PORT = os.getenv("POSTGRES_PORT", "5432")
POSTGRES_USER = os.getenv("POSTGRES_USER", "il15")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "il15_password")
POSTGRES_DB_WAREHOUSE = os.getenv("POSTGRES_DB_WAREHOUSE", "warehouse")
JDBC_URL = f"jdbc:postgresql://{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB_WAREHOUSE}"

BUCKETS = ("bronze", "silver", "gold", "models", "checkpoints")


def s3a(bucket, *parts):
    """s3a('bronze', 'messages') -> 's3a://bronze/messages'."""
    return "s3a://" + "/".join([bucket, *[p.strip("/") for p in parts]])
