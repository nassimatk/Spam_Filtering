# superset/ — Tableau de bord Superset

**Propriétaire : Étudiant 4 (E4)** · Tâches de la feuille de route : E4-01, E4-07 à E4-10

## Mission
Tableau de bord Superset.

## Fichiers prévus (à écrire)
- `Dockerfile` — Image Superset
- `superset_config.py` — Configuration Superset
- `bootstrap.sh` — Initialisation : compte admin, connexion au Gold, import du dashboard

## À faire
1. Mettre Superset dans docker-compose.yml et le connecter au Gold
2. Construire les graphiques : taux de spam, spam par jour, expéditeurs suspects, qualité du modèle
3. Ajouter des alertes visibles (seuils)
4. Exporter le dashboard dans `dashboards/` pour l'import automatique

## Interfaces
Fournit : dashboard. Reçoit : tables Gold (E2), scénarios de démo (E1).
Les noms (topic, buckets, tables, DAG) sont dans [`docs/contrat_interface.md`](../docs/contrat_interface.md).

## Notes de l'étudiant
<!-- Décisions, commandes utiles, problèmes rencontrés : à compléter au fil du projet -->
