#!/bin/sh
# Création des buckets MinIO (idempotent). Propriétaire : E2.
set -e
until mc alias set local http://minio:9000 "$MINIO_ROOT_USER" "$MINIO_ROOT_PASSWORD" > /dev/null 2>&1; do
  echo "En attente de MinIO..."; sleep 2
done
for bucket in bronze silver gold models checkpoints; do
  mc mb --ignore-existing "local/$bucket"
done
echo "Buckets disponibles :"
mc ls local
