# data/

Jeux de données locaux, **non versionnés** (voir `.gitignore`). Propriétaire : E1.

- `raw/` : fichiers sources (SMSSpamCollection, CSV d'e-mails étiquetés).
- `processed/` : `train.jsonl` et `live.jsonl`, générés par `producer/prepare_data.py` (`make data`).

Ce dossier est monté dans le conteneur `producer` sur `/data`.
