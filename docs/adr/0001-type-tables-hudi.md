# ADR-0001 — Type des tables Hudi : Copy-on-Write ou Merge-on-Read

- **Statut :** proposée (E2) — **à valider avec E3 en phase P2**, après un test d'écriture réel
- **Auteur :** Étudiant 2
- **Contexte :** les tables Silver et Gold reçoivent des upserts. Le flux est continu (micro-lots d'environ 10 secondes), mais
  le volume reste petit (jeux de données de quelques milliers de messages, rejoués).
- **Options :**
  1. **Copy-on-Write (COW)** : chaque mise à jour réécrit les fichiers Parquet concernés. Lecture simple et rapide ;
     écriture plus coûteuse, sans importance à notre échelle.
  2. **Merge-on-Read (MoR)** : les changements vont dans des fichiers log, fusionnés à la lecture ou par compaction.
     Écriture plus rapide ; lecture plus complexe et compaction à configurer.
- **Décision proposée :** **COW pour toutes les tables.** Plus simple à expliquer, à interroger (Spark SQL, copie vers
  PostgreSQL) et à maintenir, sans tâche de compaction.
- **Conséquences :** si la latence d'écriture de `messages_scored` devient un problème, repasser **cette table seule** en MoR
  et documenter la mesure (avant / après) dans le rapport.
- **À vérifier en P2 :** durée d'un micro-lot d'écriture avec COW ; nombre de petits fichiers générés.
