# Matrice de versions (E2 + E3)

Spark, Hadoop (S3A), Hudi et le connecteur Kafka doivent être **compatibles entre eux**. Les versions ci-dessous sont
celles **proposées** ; elles ne sont « validées » qu'après un test réussi (`lakehouse/test_hudi_minio.py`).

| Composant | Version proposée | Où l'installer | Validé le / par |
|---|---|---|---|
| Spark | 3.4.1 (Scala 2.12, Python 3) | image `apache/spark:3.4.1-python3` (`spark/Dockerfile`, E3) | |
| Hudi (bundle) | `hudi-spark3.4-bundle_2.12` 0.14.1 | JAR dans `/opt/spark/jars` | |
| Hadoop AWS (S3A) | `hadoop-aws` 3.3.4 | JAR dans `/opt/spark/jars` | |
| AWS SDK | `aws-java-sdk-bundle` 1.12.262 | JAR dans `/opt/spark/jars` | |
| Connecteur Kafka pour Spark | `spark-sql-kafka-0-10_2.12` 3.4.1 + `spark-token-provider-kafka-0-10_2.12` 3.4.1 | JAR | |
| Client Kafka | `kafka-clients` 3.3.2, `commons-pool2` 2.11.1 | JAR | |
| Pilote JDBC PostgreSQL | `postgresql` 42.7.3 | JAR | |
| Kafka | `apache/kafka:3.7.0` (KRaft) | `docker-compose.yml` (E1) | |
| MinIO | `minio/minio:latest` → **épingler une version précise une fois testée** | `docker-compose.yml` (E2) | |
| PostgreSQL | 16 | `docker-compose.yml` | |

Les JAR sont téléchargés depuis Maven Central (`https://repo1.maven.org/maven2/…`) et copiés dans l'image Spark (Dockerfile d'E3).
**Règle :** une montée de version se fait dans une pull request dédiée, après un nouveau passage du test.

## Réglages Spark nécessaires (déjà dans `lakehouse/spark_conf.py`)
- S3A : `endpoint`, clés d'accès, **`path.style.access=true`** (obligatoire avec MinIO), SSL désactivé.
- Hudi : `KryoSerializer`, `HoodieSparkSessionExtension`, `HoodieCatalog`, `HoodieSparkKryoRegistrar`.
