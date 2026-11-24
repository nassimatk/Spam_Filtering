# Parcours d'un message (à savoir expliquer en entier)

Exemple : un SMS `{"message_id":"a3f9…","sender":"+212612345678","body":"WIN a FREE prize","label":"spam"}`.

| # | Étape | Qui | Ce qui se passe | Où |
|---|---|---|---|---|
| 1 | Production | E1 | Le producteur publie le message dans le topic `messages` (clé = `sender`) | Kafka |
| 2 | Bronze | E3 (format : E2) | Le message est écrit **brut** avec ses métadonnées Kafka | `s3a://bronze/messages/` |
| 3 | Silver | E3 (table : E2) | Nettoyage, variables dérivées, dédoublonnage, **upsert** | `messages_silver` |
| 4 | Modèle | E3 | Entraînement sur les messages étiquetés ; modèle sauvegardé | `s3a://models/spam/<version>` |
| 5 | Classification | E3 | Le message est classé spam / ham en continu | `messages_scored` |
| 6 | Gold | E3 (table : E2) | Agrégation par jour et par expéditeur | `gold_spam_daily_sender` |
| 7 | Exposition | E2 | Copie du Gold vers PostgreSQL | base `warehouse` |
| 8 | Orchestration | E4 | Airflow planifie les étapes 3, 4 et 6 | DAG |
| 9 | Restitution | E4 | Le dashboard affiche taux de spam et expéditeurs suspects | Superset |

## Ce qui est de ma responsabilité (E2)

- Les **buckets** et leur organisation (étape 2).
- Le **format Bronze** (étape 2) et les **tables Hudi** Silver / Gold (étapes 3, 5, 6).
- La **configuration Spark ↔ MinIO / Hudi** (`spark_conf.py`) et le **writer** `upsert` utilisés par E3.
- L'**accès du dashboard au Gold** (étape 7).
- La **démonstration Hudi** : upsert, time travel, requête incrémentale.

## Questions que le jury peut poser sur le parcours

1. Pourquoi ne pas écrire directement dans Silver depuis Kafka ? *(Bronze permet de rejouer et garde la vérité brute.)*
2. Que se passe-t-il si le même message arrive deux fois ? *(L'upsert Hudi garde une seule ligne, grâce à la clé et à la précombinaison.)*
3. Comment retrouver l'état de Silver d'hier ? *(Time travel.)*
