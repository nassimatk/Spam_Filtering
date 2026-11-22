"""Schéma du message tel qu'il circule dans Kafka (contrat : docs/schema_message.md)."""
from pyspark.sql.types import StringType, StructField, StructType

MESSAGE_SCHEMA = StructType([
    StructField("message_id", StringType(), False),
    StructField("source", StringType(), True),      # sms | email
    StructField("sender", StringType(), True),
    StructField("subject", StringType(), True),
    StructField("body", StringType(), True),
    StructField("event_ts", StringType(), True),    # ISO 8601, converti en timestamp en Silver
    StructField("label", StringType(), True),       # spam | ham (vérité terrain, jamais une entrée du modèle)
])
