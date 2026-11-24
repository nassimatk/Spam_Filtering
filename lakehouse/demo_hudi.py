"""Démonstration Hudi pour la soutenance (propriétaire : E2).

Scénario (< 3 minutes) :
  1. on écrit un message ;
  2. on réécrit le MÊME message_id avec un contenu modifié : la table garde UNE seule ligne (upsert) ;
  3. time travel : on relit la table telle qu'elle était après la 1re écriture (ancienne valeur) ;
  4. requête incrémentale : seulement les changements depuis la 1re écriture.

Lancement (depuis le conteneur Spark d'E3) :
  docker compose exec spark-client /opt/spark/bin/spark-submit --master spark://spark-master:7077 \
      /opt/app/lakehouse/demo_hudi.py
"""
import time

from lakehouse.hudi_writer import read_as_of, read_incremental, read_snapshot, upsert
from lakehouse.spark_conf import get_spark
from lakehouse.tables import HudiTable

DEMO = HudiTable("demo_messages", "silver", "message_id", "ingest_ts", "event_date")
COLS = ["message_id", "body", "label", "ingest_ts", "_hoodie_commit_time"]


def show(title, df):
    print(f"\n=== {title} ===")
    df.select([c for c in COLS if c in df.columns]).show(truncate=False)


def main():
    spark = get_spark("demo_hudi")
    mid = f"demo-{int(time.time())}"   # identifiant unique : la démo peut être relancée

    def make(body, label, ts):
        return spark.createDataFrame(
            [(mid, "sms", "+212600000000", body, label, "2026-11-20", ts)],
            "message_id string, source string, sender string, body string, label string, "
            "event_date string, ingest_ts string",
        )

    # 1. première écriture
    upsert(make("Salut, on se voit ce soir ?", "ham", "2026-11-20 10:00:00"), DEMO)
    snap1 = read_snapshot(spark, DEMO).filter(f"message_id = '{mid}'")
    show("1. Après la 1re écriture", snap1)
    instant1 = snap1.agg({"_hoodie_commit_time": "max"}).first()[0]
    time.sleep(2)

    # 2. même clé, contenu modifié, ingest_ts plus récent -> UPSERT
    upsert(make("GAGNEZ un prix gratuit !!!", "spam", "2026-11-20 10:05:00"), DEMO)
    snap2 = read_snapshot(spark, DEMO).filter(f"message_id = '{mid}'")
    show("2. Après l'upsert : UNE seule ligne, valeur la plus récente", snap2)
    print(f"Nombre de lignes pour {mid} : {snap2.count()} (attendu : 1)")

    # 3. time travel
    old = read_as_of(spark, DEMO, instant1).filter(f"message_id = '{mid}'")
    show(f"3. Time travel à l'instant {instant1} : ancienne valeur", old)

    # 4. requête incrémentale
    inc = read_incremental(spark, DEMO, instant1).filter(f"message_id = '{mid}'")
    show(f"4. Incrémental depuis {instant1} : seulement le changement", inc)

    spark.stop()


if __name__ == "__main__":
    main()
