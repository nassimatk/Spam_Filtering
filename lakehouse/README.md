# lakehouse/ — Data Lake MinIO et Lakehouse Hudi

**Propriétaire : Étudiant 2 (E2)** · Tâches de la feuille de route : E2-01 à E2-12

## Mission
Data Lake MinIO et Lakehouse Hudi.

## Fichiers prévus (à écrire)
- `__init__.py` — Rend le dossier importable par les jobs Spark
- `init_minio.sh` — Création des buckets MinIO (bronze, silver, gold, models, checkpoints)
- `config.py` — Variables d'environnement communes (S3, Kafka, PostgreSQL)
- `schemas.py` — Schéma Spark du message (contrat)
- `tables.py` — Catalogue des tables Hudi : clé, précombinaison, partition, type COW/MoR
- `hudi_writer.py` — upsert(), lecture snapshot, time travel, requête incrémentale
- `spark_conf.py` — get_spark() : SparkSession configurée pour MinIO (S3A) et Hudi
- `gold_export.py` — Copie du Gold vers PostgreSQL pour Superset
- `demo_hudi.py` — Démonstration Hudi pour la soutenance

## À faire
1. Mettre MinIO dans docker-compose.yml, créer les buckets
2. Fournir la configuration S3A et la matrice de versions à E3
3. Définir les tables Hudi Silver / Gold et un writer d'upsert réutilisable
4. Préparer la démonstration Hudi (upsert, time travel, requête incrémentale) et l'accès du dashboard au Gold

## Interfaces
Fournit : stockage, writer Hudi, schémas, Gold accessible. Reçoit : besoins d'écriture (E3), colonnes du dashboard (E4).
Les noms (topic, buckets, tables, DAG) sont dans [`docs/contrat_interface.md`](../docs/contrat_interface.md).

## Notes de l'étudiant
<!-- Décisions, commandes utiles, problèmes rencontrés : à compléter au fil du projet -->
