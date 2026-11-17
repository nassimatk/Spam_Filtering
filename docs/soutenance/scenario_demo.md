# Scénario de démonstration (à répéter au moins deux fois)

Préparation : plateforme déjà démarrée (`make up` fait avant), modèle promu, quelques jours de données en Silver/Gold.

| # | Qui | Action | Preuve visible |
|---|---|---|---|
| 1 | Tous | Montrer la commande `docker compose up` et `make ps` | services *healthy* |
| 2 | E1 | Producteur actif ; Kafka UI → topic `messages` | messages qui arrivent |
| 3 | E2 | MinIO : fichiers Bronze ; démo Hudi (upsert, time travel, incrémental) | une seule ligne après doublon |
| 4 | E3 | Spark UI : jobs de streaming ; table `messages_scored` ; métriques du modèle | prédictions en continu |
| 5 | E4 | Airflow : déclencher `model_retrain_weekly`, montrer l'exécution et la promotion | DAG vert |
| 6 | E4 + E1 | Lancer `producer.py --scenario spam_burst` ; Superset : pic de spam, expéditeur suspect | alerte visible |

**Plan B :** captures d'écran / courte vidéo de chaque étape, base déjà chargée.
**Rappel guide :** démonstration testée à l'avance ; absent sans justification = 0 au projet.
