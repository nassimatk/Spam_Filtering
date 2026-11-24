"""Test d'intégration E2 : Spark <-> MinIO (S3A) <-> Hudi. À lancer dans le conteneur Spark d'E3.

  docker compose exec spark-client /opt/spark/bin/spark-submit --master spark://spark-master:7077 \
      /opt/app/lakehouse/test_hudi_minio.py

Vérifie : (1) écriture / lecture Parquet sur MinIO ; (2) écriture Hudi ; (3) UPSERT : même message_id écrit
deux fois => une seule ligne, avec la valeur la plus récente. Sortie en erreur (code 1) si un test échoue.
"""
import sys
import time

from lakehouse import config
from lakehouse.hudi_writer import read_snapshot, upsert
from lakehouse.spark_conf import get_spark
from lakehouse.tables import HudiTable

TEST_TABLE = HudiTable("_test_upsert", "silver", "message_id", "ingest_ts", "event_date")


def check(name, ok, detail=""):
    print(f"[{'OK' if ok else 'KO'}] {name} {detail}")
    return ok


def main():
    spark = get_spark("test_hudi_minio")
    results = []

    # 1. Parquet sur MinIO
    path = config.s3a("bronze", "_test", f"parquet_{int(time.time())}")
    spark.createDataFrame([(1, "a"), (2, "b")], "id int, v string").write.parquet(path)
    n = spark.read.parquet(path).count()
    results.append(check("MinIO : écriture + lecture Parquet", n == 2, f"({n} lignes)"))

    # 2 et 3. Hudi + upsert
    mid = f"test-{int(time.time())}"
    schema = "message_id string, body string, event_date string, ingest_ts string"
    upsert(spark.createDataFrame([(mid, "version A", "2026-11-20", "2026-11-20 10:00:00")], schema), TEST_TABLE)
    rows = read_snapshot(spark, TEST_TABLE).filter(f"message_id = '{mid}'").collect()
    results.append(check("Hudi : écriture initiale", len(rows) == 1))

    upsert(spark.createDataFrame([(mid, "version B", "2026-11-20", "2026-11-20 10:05:00")], schema), TEST_TABLE)
    rows = read_snapshot(spark, TEST_TABLE).filter(f"message_id = '{mid}'").collect()
    results.append(check("Hudi : upsert => UNE seule ligne", len(rows) == 1, f"({len(rows)} ligne(s))"))
    results.append(check("Hudi : upsert => valeur la plus récente",
                         len(rows) == 1 and rows[0]["body"] == "version B"))

    spark.stop()
    print("TOUS LES TESTS OK" if all(results) else "ECHEC : voir les [KO] ci-dessus")
    return 0 if all(results) else 1


if __name__ == "__main__":
    sys.exit(main())
