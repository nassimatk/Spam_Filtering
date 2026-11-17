# ADR-XXXX — Titre de la décision

- **Statut :** proposée / acceptée / remplacée
- **Date :**
- **Auteur :**
- **Contexte :** quel problème, quelles contraintes ?
- **Options envisagées :**
- **Décision :**
- **Conséquences :**

Décisions à prendre et à documenter ici (phase P0-P1) :
1. Étiquettes du jeu Enron (version étiquetée ou source « ham » seulement)
2. Comment Superset lit le Gold (copie PostgreSQL ou Spark Thrift Server)
3. Comment Airflow lance les jobs Spark (docker exec, SparkSubmitOperator…)
4. Copy-on-Write ou Merge-on-Read pour les tables Hudi
