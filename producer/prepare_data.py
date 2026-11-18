"""Propriétaire : E1 — Normalise Enron + SMS vers le schéma commun ; produit train.jsonl et live.jsonl
"""
"""E1 - Normalise SMS (+ Enron étiqueté si présent) vers le schéma commun."""
import csv
import hashlib
import json
import os
import random
import sys
from collections import defaultdict
from datetime import datetime, timedelta, timezone
from pathlib import Path

DATA = Path(os.getenv("DATA_DIR", "/data"))
RAW, OUT = DATA / "raw", DATA / "processed"
rng = random.Random(42)                      # graine fixe = reproductible
ANCHOR = datetime(2026, 11, 1, tzinfo=timezone.utc)

# Le spam est concentré sur peu d'expéditeurs pour un dashboard parlant
POOLS = {
    ("sms", "spam"):   [f"+2126{rng.randint(10**7, 10**8 - 1)}" for _ in range(15)],
    ("sms", "ham"):    [f"+2126{rng.randint(10**7, 10**8 - 1)}" for _ in range(300)],
    ("email", "spam"): [f"promo{i}@shop-x.com" for i in range(15)],
    ("email", "ham"):  [f"user{i}@entreprise.com" for i in range(300)],
}

def load_sms():
    f = RAW / "SMSSpamCollection"
    rows = []
    if not f.exists():
        return rows
    for line in f.read_text(encoding="utf-8", errors="replace").splitlines():
        if "\t" not in line:
            continue
        label, body = line.split("\t", 1)
        if label in ("ham", "spam") and body.strip():
            rows.append({"source": "sms", "subject": None,
                         "body": body.strip(), "label": label})
    return rows

def load_enron():
    """Optionnel : CSV étiqueté 'Enron-Spam' (Subject, Message, Spam/Ham, Date)."""
    f = RAW / "enron_spam.csv"
    if not f.exists():
        return []
    csv.field_size_limit(sys.maxsize)
    rows = []
    with f.open(newline="", encoding="utf-8", errors="replace") as fh:
        for r in csv.DictReader(fh):
            label = (r.get("Spam/Ham") or "").strip().lower()
            body = (r.get("Message") or "").strip()
            if label in ("ham", "spam") and body:
                rows.append({"source": "email", "subject": r.get("Subject") or None,
                             "body": body[:5000], "label": label})
    return rows

def build(row):
    ts = ANCHOR - timedelta(seconds=rng.randint(0, 30 * 24 * 3600))
    mid = hashlib.sha1(f"{row['source']}|{row['body']}".encode()).hexdigest()[:16]
    return {"message_id": mid, "source": row["source"],
            "sender": rng.choice(POOLS[(row["source"], row["label"])]),
            "subject": row["subject"], "body": row["body"],
            "event_ts": ts.strftime("%Y-%m-%dT%H:%M:%SZ"), "label": row["label"]}

def main():
    rows = load_sms() + load_enron()
    if not rows:
        sys.exit("Aucune donnée dans data/raw/ (SMSSpamCollection attendu)")
    recs = {}
    for row in rows:
        r = build(row)
        recs[r["message_id"]] = r            # dédoublonnage par message_id
    groups = defaultdict(list)
    for r in recs.values():
        groups[(r["source"], r["label"])].append(r)
    train, live = [], []
    for key in sorted(groups):               # découpe stratifiée
        g = sorted(groups[key], key=lambda r: r["message_id"])
        rng.shuffle(g)
        cut = int(len(g) * 0.8)
        train += g[:cut]
        live += g[cut:]
    OUT.mkdir(parents=True, exist_ok=True)
    for name, data in (("train", train), ("live", live)):
        data.sort(key=lambda r: r["event_ts"])
        with (OUT / f"{name}.jsonl").open("w", encoding="utf-8") as f:
            for r in data:
                f.write(json.dumps(r, ensure_ascii=False) + "\n")
        print(f"{name}.jsonl : {len(data)} messages")

if __name__ == "__main__":
    main()