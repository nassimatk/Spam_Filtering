# Matrice de versions (E2 + E3, phase P1)

Spark, Hadoop (S3A), Hudi et le connecteur Kafka doivent être compatibles entre eux : c'est la panne n°1 du projet.
**Statut : proposition d'E2, à valider avec E3 après le test `lakehouse/smoke_test_s3a.py`.**

| Composant | Version proposée | Coordonnée / image | Validé le / par |
|---|---|---|---|
| Spark | 3.5.1 (Scala 2.12) | `apache/spark:3.5.1` ou `pyspark==3.5.1` | |
| Hudi (bundle) | 0.15.0 | `org.apache.hudi:hudi-spark3.5-bundle_2.12:0.15.0` | |
| Hadoop AWS | 3.3.4 (celle livrée avec Spark 3.5.1) | `org.apache.hadoop:hadoop-aws:3.3.4` | |
| AWS SDK | 1.12.262 (liée à hadoop-aws 3.3.4) | `com.amazonaws:aws-java-sdk-bundle:1.12.262` | |
| Connecteur Kafka pour Spark | 3.5.1 | `org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.1` | |
| Kafka | 3.7.0 | `apache/kafka:3.7.0` (choix d'E1) | |
| MinIO | RELEASE.2024-06-13T22-53-53Z | `minio/minio:RELEASE.2024-06-13T22-53-53Z` | |
| Client MinIO (mc) | RELEASE.2024-06-12T14-34-03Z | `minio/mc:RELEASE.2024-06-12T14-34-03Z` | |
| PostgreSQL | | à remplir par le propriétaire de postgres | |
| Airflow | | à remplir par E4 | |
| Superset | | à remplir par E4 | |

## Règles
- `hadoop-aws` doit avoir **exactement** la version de Hadoop embarquée par Spark (3.3.4 pour Spark 3.5.x).
- Le bundle Hudi doit correspondre à la version mineure de Spark (`hudi-spark3.5-bundle` pour Spark 3.5).
- Un changement de version est annoncé à l'équipe et reporté ici dans la même pull request.

## Liste pour `SPARK_JARS_PACKAGES` (essai sans image préparée)
```
org.apache.hudi:hudi-spark3.5-bundle_2.12:0.15.0,org.apache.hadoop:hadoop-aws:3.3.4,com.amazonaws:aws-java-sdk-bundle:1.12.262,org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.1
```
