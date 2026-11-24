"""Copie du Gold vers PostgreSQL pour Superset (décision : docs/adr/0001-gold-vers-superset.md).

Le Gold de référence reste dans Hudi ; PostgreSQL (base « warehouse ») n'est qu'une vue de
consommation pour le dashboard. Propriétaire : E2.
"""
from lakehouse import config


def export_to_postgres(df, table, mode="overwrite"):
    """mode='overwrite' : remplace le contenu (la table et ses droits sont conservés : truncate)."""
    writer = (
        df.write.format("jdbc")
        .option("url", config.JDBC_URL)
        .option("dbtable", table)
        .option("user", config.POSTGRES_USER)
        .option("password", config.POSTGRES_PASSWORD)
        .option("driver", "org.postgresql.Driver")
    )
    if mode == "overwrite":
        writer = writer.option("truncate", "true")
    writer.mode(mode).save()
    print(f"[export] table PostgreSQL {table} ({mode})")
