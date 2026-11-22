"""Lecture / écriture Hudi réutilisables par tous les jobs Spark (propriétaire : E2)."""
from lakehouse.tables import TABLES, HudiTable

COMPLEX_KEYGEN = "org.apache.hudi.keygen.ComplexKeyGenerator"
NONPARTITIONED_KEYGEN = "org.apache.hudi.keygen.NonpartitionedKeyGenerator"


def _table(table):
    return table if isinstance(table, HudiTable) else TABLES[table]


def hudi_options(table, operation="upsert"):
    t = _table(table)
    opts = {
        "hoodie.table.name": t.name,
        "hoodie.datasource.write.recordkey.field": t.recordkey,
        "hoodie.datasource.write.precombine.field": t.precombine,
        "hoodie.datasource.write.table.type": t.table_type,
        "hoodie.datasource.write.operation": operation,
        "hoodie.datasource.write.hive_style_partitioning": "true",
        "hoodie.upsert.shuffle.parallelism": "2",
        "hoodie.insert.shuffle.parallelism": "2",
        "hoodie.datasource.hive_sync.enable": "false",
    }
    if t.partition:
        opts["hoodie.datasource.write.partitionpath.field"] = t.partition
        if "," in t.recordkey:
            opts["hoodie.datasource.write.keygenerator.class"] = COMPLEX_KEYGEN
    else:
        opts["hoodie.datasource.write.keygenerator.class"] = NONPARTITIONED_KEYGEN
    return opts


def upsert(df, table, mode="append"):
    """Upsert d'un DataFrame dans une table Hudi : un doublon de clé n'ajoute pas de ligne."""
    t = _table(table)
    if df.isEmpty():
        print(f"[hudi] {t.name} : rien à écrire")
        return
    df.write.format("hudi").options(**hudi_options(t)).mode(mode).save(t.path)
    print(f"[hudi] upsert dans {t.name} ({t.path})")


def read_snapshot(spark, table):
    """Vue la plus récente de la table."""
    return spark.read.format("hudi").load(_table(table).path)


def read_as_of(spark, table, instant):
    """Time travel : état de la table à un instant (ex. '2026-11-20 10:30:00' ou '20261120103000')."""
    return spark.read.format("hudi").option("as.of.instant", instant).load(_table(table).path)


def read_incremental(spark, table, begin_instant):
    """Requête incrémentale : seulement les changements après `begin_instant`."""
    return (spark.read.format("hudi")
            .option("hoodie.datasource.query.type", "incremental")
            .option("hoodie.datasource.read.begin.instanttime", begin_instant)
            .load(_table(table).path))
