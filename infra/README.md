# infra/

Éléments d'infrastructure partagés (propriétaires : tous).

- `postgres/init-databases.sh` : crée les bases `airflow`, `superset`, `warehouse` à la première initialisation du volume.
- `scripts/smoke_test.sh` : test de fumée (`make smoke`).
