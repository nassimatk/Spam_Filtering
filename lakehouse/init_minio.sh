#!/bin/sh
# Propriétaire : E2 — Création des buckets MinIO (bronze, silver, gold, models, checkpoints)
#
# Lancé par le service Compose `minio-init` (image minio/mc), une fois MinIO prêt.
# Idempotent : on peut le relancer sans risque (--ignore-existing).
set -eu

ENDPOINT="${MINIO_ENDPOINT:-http://minio:9000}"
: "${MINIO_ROOT_USER:?MINIO_ROOT_USER manquant (voir .env)}"
: "${MINIO_ROOT_PASSWORD:?MINIO_ROOT_PASSWORD manquant (voir .env)}"

# Noms figés dans docs/contrat_interface.md : ne pas les changer ici sans prévenir l'équipe.
BUCKETS="bronze silver gold models checkpoints"

# Attendre que MinIO accepte les connexions (30 essais x 2 s)
essai=0
until mc alias set local "$ENDPOINT" "$MINIO_ROOT_USER" "$MINIO_ROOT_PASSWORD" >/dev/null 2>&1; do
  essai=$((essai + 1))
  if [ "$essai" -ge 30 ]; then
    echo "[minio-init] MinIO injoignable sur $ENDPOINT" >&2
    exit 1
  fi
  sleep 2
done

for bucket in $BUCKETS; do
  mc mb --ignore-existing "local/$bucket"
done

echo "[minio-init] buckets disponibles :"
mc ls local
