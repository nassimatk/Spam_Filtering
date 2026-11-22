# ADR-0002 — Comment Superset lit le Gold

- **Statut :** proposée (E2) — **à valider avec E4 avant la fin de la phase P1**
- **Auteur :** Étudiant 2
- **Contexte :** Superset ne lit pas directement les tables Hudi stockées sur MinIO : il lui faut une couche d'accès SQL.
- **Options :**
  1. **Copie du Gold vers PostgreSQL** (JDBC) après chaque construction ; Superset interroge la base `warehouse`.
  2. **Spark Thrift Server** avec synchronisation du catalogue Hive ; Superset s'y connecte via PyHive.
- **Décision proposée :** option 1. Le Gold de référence reste dans Hudi ; `lakehouse/gold_export.py` en écrit une copie
  dans PostgreSQL. Plus simple, robuste, et peu gourmande en mémoire.
- **Conséquences :** la fraîcheur du dashboard dépend de l'exécution de `build_gold` (DAG `gold_batch_daily`, E4).
  Les noms de tables PostgreSQL sont identiques à ceux du Gold Hudi.
- **Alternative :** option 2 si l'équipe veut une démonstration « pur Lakehouse » ; plus lourd et plus fragile.
