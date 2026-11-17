# producer/ — Sources de données et ingestion Kafka

**Propriétaire : Étudiant 1 (E1)** · Tâches de la feuille de route : E1-01 à E1-13

## Mission
Sources de données et ingestion Kafka.

## Fichiers prévus (à écrire)
- `Dockerfile` — Image du conteneur « producer » (Python + client Kafka)
- `requirements.txt` — Dépendances Python du producteur
- `entrypoint.sh` — Point d'entrée : prépare les données si absentes, puis lance le producteur
- `prepare_data.py` — Normalise Enron + SMS vers le schéma commun ; produit train.jsonl et live.jsonl
- `producer.py` — Rejoue les messages dans le topic Kafka (débit configurable, scénario de pic de spam)
- `kafka/init-topics.sh` — Création des topics Kafka (messages, messages_dlq)

## À faire
1. Préparer les jeux de données étiquetés (train / live) au schéma commun
2. Mettre Kafka dans docker-compose.yml et créer le topic `messages`
3. Écrire le producteur Python (débit configurable) et le conteneuriser
4. Tester le flux, préparer un scénario de pic de spam pour la démo

## Interfaces
Fournit : topic `messages`, jeux train / live. Reçoit : schéma du message validé par les 4.
Les noms (topic, buckets, tables, DAG) sont dans [`docs/contrat_interface.md`](../docs/contrat_interface.md).

## Notes de l'étudiant
<!-- Décisions, commandes utiles, problèmes rencontrés : à compléter au fil du projet -->
