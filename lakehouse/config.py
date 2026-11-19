"""Propriétaire : E2 — Variables d'environnement communes (S3, Kafka, PostgreSQL)

Les valeurs viennent de l'environnement (docker-compose.yml / .env) : jamais de secret dans le code.
Les noms (buckets, topic) sont figés dans docs/contrat_interface.md.
"""
import os

BUCKETS = ("bronze", "silver", "gold", "models", "checkpoints")

# --- S3 / MinIO ------------------------------------------------------------
S3_ENDPOINT = os.environ.get("S3_ENDPOINT", "http://minio:9000")

# --- Kafka -----------------------------------------------------------------
KAFKA_BOOTSTRAP = os.environ.get("KAFKA_BOOTSTRAP", "kafka:9092")
KAFKA_TOPIC = os.environ.get("KAFKA_TOPIC", "messages")

# --- PostgreSQL (copie du Gold pour Superset) ---------------------------------
POSTGRES_HOST = os.environ.get("POSTGRES_HOST", "postgres")
POSTGRES_PORT = int(os.environ.get("POSTGRES_PORT", "5432"))
POSTGRES_DB = os.environ.get("POSTGRES_DB", "warehouse")
POSTGRES_USER = os.environ.get("POSTGRES_USER", "")
POSTGRES_PASSWORD = os.environ.get("POSTGRES_PASSWORD", "")


def s3_credentials():
    """Retourne (clé d'accès, clé secrète).

    Lit S3_ACCESS_KEY / S3_SECRET_KEY, sinon MINIO_ROOT_USER / MINIO_ROOT_PASSWORD.
    """
    access = os.environ.get("S3_ACCESS_KEY") or os.environ.get("MINIO_ROOT_USER")
    secret = os.environ.get("S3_SECRET_KEY") or os.environ.get("MINIO_ROOT_PASSWORD")
    if not access or not secret:
        raise RuntimeError(
            "Identifiants MinIO absents : définir S3_ACCESS_KEY et S3_SECRET_KEY "
            "(ou MINIO_ROOT_USER et MINIO_ROOT_PASSWORD) dans l'environnement du service."
        )
    return access, secret


def s3a_path(bucket, *parts):
    """Construit un chemin S3A : s3a_path('silver', 'messages_silver') -> 's3a://silver/messages_silver'."""
    if bucket not in BUCKETS:
        raise ValueError("Bucket inconnu : %s (attendu : %s)" % (bucket, ", ".join(BUCKETS)))
    return "s3a://" + "/".join((bucket,) + tuple(parts))
