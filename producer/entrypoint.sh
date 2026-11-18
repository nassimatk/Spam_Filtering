#!/bin/bash
set -e
if [ ! -f /data/processed/live.jsonl ]; then
  python prepare_data.py
fi
exec python producer.py
