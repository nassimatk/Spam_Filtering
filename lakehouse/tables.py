"""Catalogue des tables Hudi du Lakehouse (propriétaire : E2).

Toute modification (clé, précombinaison, partition, type) doit être annoncée à E3 et E4.
Silver et Gold sont des tables Hudi dans les buckets MinIO du même nom.
"""
from dataclasses import dataclass

from lakehouse.config import s3a


@dataclass(frozen=True)
class HudiTable:
    name: str
    bucket: str
    recordkey: str          # plusieurs champs séparés par une virgule => clé composite
    precombine: str         # en cas de doublon, la ligne avec la plus grande valeur gagne
    partition: str = ""     # vide => table non partitionnée
    table_type: str = "COPY_ON_WRITE"   # ou MERGE_ON_READ (à justifier dans le rapport)

    @property
    def path(self):
        return s3a(self.bucket, self.name)


TABLES = {
    # Silver : messages nettoyés et dédoublonnés
    "messages_silver": HudiTable("messages_silver", "silver", "message_id", "ingest_ts", "event_date"),
    # Silver : prédictions du modèle (une ligne par message classé)
    "messages_scored": HudiTable("messages_scored", "silver", "message_id", "scored_ts", "event_date"),
    # Gold : indicateurs par jour et par expéditeur
    "gold_spam_daily_sender": HudiTable(
        "gold_spam_daily_sender", "gold", "event_date,sender", "computed_at", "event_date"),
    # Gold : historique des métriques du modèle (précision, rappel...)
    "gold_model_metrics": HudiTable("gold_model_metrics", "gold", "run_id", "created_at"),
}
