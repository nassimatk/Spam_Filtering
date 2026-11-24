from lakehouse.config import s3a
from lakehouse.hudi_writer import COMPLEX_KEYGEN, NONPARTITIONED_KEYGEN, hudi_options
from lakehouse.tables import TABLES


def test_s3a_helper():
    assert s3a("bronze", "messages") == "s3a://bronze/messages"
    assert s3a("silver", "/messages_silver/") == "s3a://silver/messages_silver"


def test_catalogue_contient_les_4_tables_du_contrat():
    assert set(TABLES) == {"messages_silver", "messages_scored", "gold_spam_daily_sender", "gold_model_metrics"}
    for t in TABLES.values():
        assert t.path.startswith(f"s3a://{t.bucket}/")


def test_silver_options_upsert_cle_simple():
    o = hudi_options("messages_silver")
    assert o["hoodie.datasource.write.operation"] == "upsert"
    assert o["hoodie.datasource.write.recordkey.field"] == "message_id"
    assert o["hoodie.datasource.write.precombine.field"] == "ingest_ts"
    assert o["hoodie.datasource.write.partitionpath.field"] == "event_date"
    assert o["hoodie.datasource.write.table.type"] == "COPY_ON_WRITE"
    assert "hoodie.datasource.write.keygenerator.class" not in o


def test_gold_cle_composite_utilise_le_generateur_complexe():
    o = hudi_options("gold_spam_daily_sender")
    assert o["hoodie.datasource.write.recordkey.field"] == "event_date,sender"
    assert o["hoodie.datasource.write.keygenerator.class"] == COMPLEX_KEYGEN


def test_table_non_partitionnee():
    o = hudi_options("gold_model_metrics")
    assert o["hoodie.datasource.write.keygenerator.class"] == NONPARTITIONED_KEYGEN
    assert "hoodie.datasource.write.partitionpath.field" not in o
