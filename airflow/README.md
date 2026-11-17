# airflow/ — Orchestration Airflow

**Propriétaire : Étudiant 4 (E4)** · Tâches de la feuille de route : E4-02 à E4-06, E4-10, E4-11

## Mission
Orchestration Airflow.

## Fichiers prévus (à écrire)
- `Dockerfile` — Image Airflow
- `requirements.txt` — Dépendances Python des DAG
- `dags/common.py` — Outils communs aux DAG (arguments par défaut, lancement des jobs Spark)
- `dags/gold_batch_daily.py` — DAG quotidien : Bronze vers Silver puis Gold
- `dags/data_quality_daily.py` — DAG quotidien : contrôles qualité
- `dags/model_retrain_weekly.py` — DAG hebdomadaire : réentraînement, évaluation (précision, rappel), promotion

## À faire
1. Mettre Airflow dans docker-compose.yml et le relier à Spark
2. DAG de construction du Gold (quotidien)
3. DAG de contrôles qualité
4. DAG de réentraînement et d'évaluation du modèle (précision, rappel)

## Interfaces
Fournit : orchestration automatique. Reçoit : jobs Spark (E3), tables Gold (E2).
Les noms (topic, buckets, tables, DAG) sont dans [`docs/contrat_interface.md`](../docs/contrat_interface.md).

## Notes de l'étudiant
<!-- Décisions, commandes utiles, problèmes rencontrés : à compléter au fil du projet -->
