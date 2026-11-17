# Schéma du message Kafka (propriétaire : E1)

Valeur du message : JSON UTF-8. Clé Kafka : `sender`.

| Champ | Type | Obligatoire | Description | Exemple |
|---|---|---|---|---|
| `message_id` | string | oui | Identifiant stable (hash). Clé d'upsert Hudi. | `a3f9c1…` |
| `source` | string | oui | `sms` ou `email` | `sms` |
| `sender` | string | oui | Expéditeur (adresse ou numéro simulé) | `promo@shop-x.com` |
| `subject` | string/null | non | Objet (null pour un SMS) | `Gagnez un prix !` |
| `body` | string | oui | Contenu | `Cliquez ici…` |
| `event_ts` | string ISO 8601 | oui | Date d'émission (UTC). Simulée pour les SMS. | `2026-11-20T09:15:00Z` |
| `label` | string | non | Vérité terrain `spam` / `ham`. **Jamais une variable d'entrée du modèle.** | `spam` |

## Exemple
```json
{"message_id":"a3f9c1d2e4b5a601","source":"sms","sender":"+212612345678","subject":null,
 "body":"WIN a FREE prize now http://x.co","event_ts":"2026-11-20T09:15:00Z","label":"spam"}
```

## Sources et étiquettes (tâche E1-01 — à trancher en phase P0)
- **SMS Spam Collection (UCI)** : étiquetée (`ham` / `spam`). Aucun expéditeur ni date : **simulés** par
  `prepare_data.py` (le spam est concentré sur peu d'expéditeurs pour rendre le dashboard parlant).
- **Enron** : le corpus brut **n'a pas d'étiquette spam/ham**. Options : (a) version étiquetée « Enron-Spam »
  (CSV avec colonnes `Subject, Message, Spam/Ham, Date`, déposé dans `data/raw/`), (b) Enron comme source de messages
  légitimes uniquement. Décision à valider avec l'enseignant et à consigner dans `docs/adr/`.

## Jeux produits (graine fixe = reproductibles)
`data/processed/train.jsonl` (≈ 80 %, historique, mode `backfill`) et `data/processed/live.jsonl`
(≈ 20 %, rejoué en flux). Découpe stratifiée par source et par label.
