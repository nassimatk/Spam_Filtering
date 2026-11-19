import hashlib
import json
import os
import random
import signal
import time
from datetime import datetime, timezone
from pathlib import Path

from confluent_kafka import Producer

BOOT = os.getenv("KAFKA_BOOTSTRAP", "localhost:29092")
TOPIC = os.getenv("KAFKA_TOPIC", "messages")
DLQ = os.getenv("KAFKA_DLQ_TOPIC", "messages_dlq")
MODE = os.getenv("PRODUCER_MODE", "live")            # live | backfill
RATE = float(os.getenv("PRODUCER_RATE", "5"))         # messages / seconde
LOOP = os.getenv("PRODUCER_LOOP", "true").lower() == "true"
SPIKE_AFTER = int(os.getenv("SPIKE_AFTER", "0"))      # 0 = pas de pic
SPIKE_DURATION = int(os.getenv("SPIKE_DURATION", "30"))
SPIKE_SENDER = os.getenv("SPIKE_SENDER", "promo-flash@shop-x.com")
FILE = Path(os.getenv("DATA_DIR", "/data")) / "processed" / \
    ("train.jsonl" if MODE == "backfill" else "live.jsonl")
REQUIRED = ("message_id", "source", "sender", "body", "event_ts")

stop = False
def _stop(*_):
    global stop
    stop = True
signal.signal(signal.SIGINT, _stop)
signal.signal(signal.SIGTERM, _stop)

def sha(s):
    return hashlib.sha1(s.encode()).hexdigest()[:16]

def now_iso():
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

def valid(r):
    return all(r.get(k) for k in REQUIRED) and r["source"] in ("sms", "email")

def on_delivery(err, msg):
    if err:
        print("Erreur d'envoi :", err, flush=True)

def send(p, rec):
    topic = TOPIC if valid(rec) else DLQ         # invalides -> messages_dlq
    key = str(rec.get("sender") or "unknown").encode()
    value = json.dumps(rec, ensure_ascii=False).encode("utf-8")
    while True:
        try:
            p.produce(topic, key=key, value=value, on_delivery=on_delivery)
            break
        except BufferError:
            p.poll(1)
    p.poll(0)

def main():
    records = [json.loads(line) for line in FILE.open(encoding="utf-8") if line.strip()]
    spam = [r for r in records if r.get("label") == "spam"]
    p = Producer({"bootstrap.servers": BOOT, "acks": "all",
                  "enable.idempotence": True, "linger.ms": 20})
    start, sent, n = time.time(), 0, 0
    print(f"Mode={MODE} fichier={FILE} ({len(records)} messages) débit={RATE}/s", flush=True)
    while not stop:
        for rec in records:
            if stop:
                break
            rec = dict(rec)
            elapsed = time.time() - start
            spiking = (MODE == "live" and SPIKE_AFTER
                       and SPIKE_AFTER <= elapsed < SPIKE_AFTER + SPIKE_DURATION)
            if spiking:                           # pic de spam sur un expéditeur
                rec = dict(random.choice(spam))
                rec["sender"] = SPIKE_SENDER
                rec["message_id"] = sha(f"spike-{time.time_ns()}")
            elif n > 0:                           # passes suivantes : nouveaux ids
                rec["message_id"] = sha(f"{rec['message_id']}-{n}")
            if MODE == "live":
                rec["event_ts"] = now_iso()
            send(p, rec)
            sent += 1
            if sent % 100 == 0:
                print(f"{sent} messages envoyés", flush=True)
            if MODE == "live":
                time.sleep(1 / (RATE * (10 if spiking else 1)))
        n += 1
        if MODE == "backfill" or not LOOP:
            break
    p.flush(10)
    print(f"Terminé : {sent} messages envoyés", flush=True)

if __name__ == "__main__":
    main()