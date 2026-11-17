# spark/ — Traitements Spark (DataFrames, SQL, Streaming, MLlib)

**Propriétaire : Étudiant 3 (E3)** · Tâches de la feuille de route : E3-01 à E3-12

## Mission
Traitements Spark (DataFrames, SQL, Streaming, MLlib).

## Fichiers prévus (à écrire)
- `Dockerfile` — Image Spark commune (Spark + JAR Hudi, S3A, Kafka, PostgreSQL)
- `requirements.txt` — Dépendances Python de l'image Spark
- `jobs/features.py` — Nettoyage et variables dérivées (partagés entraînement / prédiction)
- `jobs/stream_bronze.py` — Streaming : Kafka vers Bronze (données brutes)
- `jobs/bronze_to_silver.py` — Batch : Bronze vers Silver (nettoyage, dédoublonnage, upsert Hudi)
- `jobs/train_model.py` — Entraînement et évaluation MLlib (TF-IDF + Naive Bayes / régression logistique)
- `jobs/promote_model.py` — Promotion d'un modèle vers « latest »
- `jobs/stream_classify.py` — Streaming : classification spam / ham en continu
- `jobs/build_gold.py` — Spark SQL : indicateurs Gold (spam par jour et par expéditeur)
- `jobs/quality_checks.py` — Contrôles qualité de la zone Silver

## À faire
1. Mettre Spark (master, worker) dans docker-compose.yml
2. Streaming Kafka vers Bronze ; batch Bronze vers Silver
3. Pipeline MLlib (TF-IDF + Naive Bayes / régression logistique), évaluation précision / rappel
4. Classification en streaming, Spark SQL pour le Gold, jobs paramétrables pour Airflow

## Interfaces
Fournit : jobs paramétrables, modèle, Silver / Gold remplis. Reçoit : Kafka (E1), MinIO / Hudi (E2).
Les noms (topic, buckets, tables, DAG) sont dans [`docs/contrat_interface.md`](../docs/contrat_interface.md).

## Notes de l'étudiant
- Démarrage : environnement local PySpark, entraînement d'abord sur SMSSpamCollection.
- Ordre de travail : features.py, train_model.py, puis Dockerfile et jobs de streaming.
- À décider avec E2 : versions Spark / Hudi / Hadoop-AWS (docs/versions.md).
