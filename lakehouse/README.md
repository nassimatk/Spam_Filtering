# lakehouse/ — Data Lake MinIO et Lakehouse Hudi

**Propriétaire : Étudiant 2 (E2)** · Tâches de la feuille de route : E2-01 à E2-12

## Mission
Organiser le stockage en zones **Bronze / Silver / Gold**, garantir des tables Hudi propres (upserts, sans doublon)
et rendre le Gold consultable par le dashboard.

## Fichiers
| Fichier | Rôle | Utilisé par |
|---|---|---|
| `init_minio.sh` | Crée les buckets `bronze`, `silver`, `gold`, `models`, `checkpoints` (service `minio-init`) | Compose |
| `config.py` | Variables d'environnement (S3, Kafka, PostgreSQL) + helper `s3a()` | tous |
| `spark_conf.py` | `get_spark()` : SparkSession configurée pour MinIO (S3A) et Hudi | **E3** |
| `schemas.py` | Schéma Spark du message (contrat) | E3 |
| `tables.py` | Catalogue des tables Hudi : clé, précombinaison, partition, type COW/MoR | E3 |
| `hudi_writer.py` | `upsert()`, `read_snapshot()`, `read_as_of()` (time travel), `read_incremental()` | **E3** |
| `gold_export.py` | Copie du Gold vers PostgreSQL pour Superset (ADR-0002) | E3, E4 |
| `test_hudi_minio.py` | Test d'intégration Spark ↔ MinIO ↔ Hudi (écriture, **upsert = 1 ligne**) | E2 |
| `demo_hudi.py` | Démonstration de soutenance : upsert, time travel, incrémental | E2 |

Ce dossier est **monté dans les conteneurs Spark** (`/opt/app/lakehouse`) : une modification est visible sans reconstruire l'image.

## Utilisation
```bash
make up-lake      # MinIO + buckets ; console http://localhost:9001
make lake-test    # test Spark <-> MinIO <-> Hudi   (nécessite le conteneur spark-client d'E3)
make lake-demo    # démonstration Hudi               (idem)
pytest -q         # tests unitaires sans Docker
```

## Dans un job Spark (exemple pour E3)
```python
from lakehouse.spark_conf import get_spark
from lakehouse.hudi_writer import upsert, read_snapshot

spark = get_spark("mon_job")
upsert(df, "messages_silver")                 # écriture sans doublon
silver = read_snapshot(spark, "messages_silver")
```

## Interfaces
- **Fournit à E3** : `get_spark()`, `upsert()`, schémas, chemins, `docs/versions.md`.
- **Fournit à E4** : tables Gold copiées dans PostgreSQL (base `warehouse`), colonnes dans `docs/contrat_interface.md`.
- **Reçoit** : schéma du message (E1), besoins d'écriture (E3), colonnes voulues pour le dashboard (E4).

## Ce que `spark/Dockerfile` (E3) doit contenir pour que tout fonctionne
Les JAR listés dans `docs/versions.md` (Hudi, hadoop-aws, AWS SDK, connecteur Kafka, JDBC PostgreSQL) dans `/opt/spark/jars`,
et le montage `./lakehouse:/opt/app/lakehouse` avec `PYTHONPATH=/opt/app`.
