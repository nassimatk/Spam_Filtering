#!/bin/bash
set -e
KT=/opt/kafka/bin/kafka-topics.sh
BOOT=kafka:9092
$KT --bootstrap-server $BOOT --create --if-not-exists \
    --topic "${KAFKA_TOPIC:-messages}" --partitions 3 --replication-factor 1
$KT --bootstrap-server $BOOT --create --if-not-exists \
    --topic messages_dlq --partitions 1 --replication-factor 1
$KT --bootstrap-server $BOOT --list