# Contrat d'interface (source de vérité des noms)

> **Règle :** on ne change pas un nom ici sans prévenir l'équipe, dans la même pull request.

## Kafka (E1)
| Élément | Valeur |
|---|---|
| Topic principal | `messages` — 3 partitions, réplication 1, **clé = `sender`** |
| File des invalides | `messages_dlq` |
| Adresse interne / externe | `kafka:9092` / `localhost:29092` |
| Format | JSON, voir [schema_message.md](schema_message.md) |

## Buckets MinIO (E2)
`bronze` · `silver` · `gold` · `models` · `checkpoints`

## Tables (E2 définit, E3 écrit)
| Table | Zone | Clé | Précombinaison | Partition | Détenue par |
|---|---|---|---|---|---|
| `messages_silver` | Silver | `message_id` | `ingest_ts` | `event_date` | E2 / E3 |
| `messages_scored` | Silver | `message_id` | `scored_ts` | `event_date` | E2 / E3 |
| `gold_spam_daily_sender` | Gold | `event_date,sender` | `computed_at` | `event_date` | E2 / E3 |
| `gold_model_metrics` | Gold | `run_id` | `created_at` | — | E2 / E3 / E4 |

Colonnes `gold_spam_daily_sender` : `event_date, sender, nb_messages, nb_spam, taux_spam, computed_at`.
Colonnes `gold_model_metrics` : `run_id, model_version, algo, created_at, n_train, n_test, accuracy, precision_spam, recall_spam, f1_spam, auc, is_promoted`.
Table PostgreSQL supplémentaire : `data_quality_checks(checked_at, check_name, status, detail)`.

Copie PostgreSQL (base `warehouse`, pour Superset) : mêmes noms que les tables Gold.

## Modèle (E3)
`s3a://models/spam/<AAAAMMJJHHMMSS>-<algo>/` ; alias de production : `s3a://models/spam/latest/`.

## DAG Airflow (E4)
| DAG | Planification | Rôle |
|---|---|---|
| `gold_batch_daily` | `@daily` | `bronze_to_silver` → `build_gold` |
| `data_quality_daily` | `@daily` | contrôles qualité de Silver |
| `model_retrain_weekly` | `@weekly` | entraîne, évalue, promeut si meilleur F1 spam |

## Jobs Spark (E3) — appelables par Airflow
Chaque job est un script de `spark/jobs/`, **paramétrable** (`--date`, `--algo`, `--version`) et **idempotent**.
`stream_bronze` et `stream_classify` sont des services Compose permanents ; les autres sont des jobs batch.

## Variables d'environnement
Définies dans `.env.example`, jamais de secret dans Git. Les services Spark lisent : `KAFKA_BOOTSTRAP`,
`KAFKA_TOPIC`, `S3_ENDPOINT`, `S3_ACCESS_KEY`, `S3_SECRET_KEY`, `POSTGRES_*` (via `lakehouse/config.py`).

## Ports hôte
Kafka 29092 · Kafka UI 8090 · MinIO 9000/9001 · Spark UI 8082 · Airflow 8080 · Superset 8088 · PostgreSQL 5432.
