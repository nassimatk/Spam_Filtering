# Proprietaire : E3
# Spark 3.4.1 + Hudi + S3A + Kafka + PostgreSQL

FROM apache/spark:3.4.1-python3

USER root

WORKDIR /opt/app

# JAR nécessaires à l'intégration avec MinIO, Hudi, Kafka et PostgreSQL
RUN mkdir -p /opt/spark/jars

ADD https://repo1.maven.org/maven2/org/apache/hudi/hudi-spark3.4-bundle_2.12/0.14.1/hudi-spark3.4-bundle_2.12-0.14.1.jar /opt/spark/jars/
ADD https://repo1.maven.org/maven2/org/apache/hadoop/hadoop-aws/3.3.4/hadoop-aws-3.3.4.jar /opt/spark/jars/
ADD https://repo1.maven.org/maven2/com/amazonaws/aws-java-sdk-bundle/1.12.262/aws-java-sdk-bundle-1.12.262.jar /opt/spark/jars/
ADD https://repo1.maven.org/maven2/org/apache/spark/spark-sql-kafka-0-10_2.12/3.4.1/spark-sql-kafka-0-10_2.12-3.4.1.jar /opt/spark/jars/
ADD https://repo1.maven.org/maven2/org/apache/spark/spark-token-provider-kafka-0-10_2.12/3.4.1/spark-token-provider-kafka-0-10_2.12-3.4.1.jar /opt/spark/jars/
ADD https://repo1.maven.org/maven2/org/apache/kafka/kafka-clients/3.3.2/kafka-clients-3.3.2.jar /opt/spark/jars/
ADD https://repo1.maven.org/maven2/org/apache/commons/commons-pool2/2.11.1/commons-pool2-2.11.1.jar /opt/spark/jars/
ADD https://repo1.maven.org/maven2/org/postgresql/postgresql/42.7.3/postgresql-42.7.3.jar /opt/spark/jars/

COPY spark/requirements.txt /opt/app/requirements.txt

RUN pip install --no-cache-dir -r /opt/app/requirements.txt

COPY lakehouse /opt/app/lakehouse
COPY spark/jobs /opt/app/jobs

ENV PYTHONPATH=/opt/app
ENV PYSPARK_PYTHON=python3

USER spark


# Données d'entraînement et de test
COPY data /opt/app/data
