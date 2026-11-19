# Notions : Data Lake, Lakehouse, Hudi

## 1. Data Lake, entrepôt, Lakehouse

| | Data Lake | Entrepôt de données | Lakehouse |
|---|---|---|---|
| **Données** | Fichiers bruts de toute forme (JSON, Parquet, CSV…) | Tables structurées | Fichiers (Parquet) **organisés en tables** |
| **Schéma** | Appliqué à la lecture | Strict, imposé à l'écriture | Imposé par le format de table |
| **Mises à jour** | Difficiles (on réécrit des fichiers) | Faciles (UPDATE, transactions) | Faciles (upsert, transactions) |
| **Coût / volume** | Peu cher, très gros volumes | Plus cher | Peu cher, très gros volumes |
| **Historique** | Non | Rarement | Oui (time travel) |

Un **Lakehouse** garde le stockage économique du Data Lake et ajoute les garanties de l'entrepôt (transactions,
mises à jour, schéma, historique) grâce à un **format de table**. Ici : **Apache Hudi** sur **MinIO** (stockage compatible S3).

## 2. Les trois zones (architecture « médaillon »)

| Zone | Contenu | Règle d'or | Dans notre projet |
|---|---|---|---|
| **Bronze** | Données brutes, telles que reçues | **Jamais modifiées** (on peut toujours rejouer) | Messages JSON de Kafka + métadonnées |
| **Silver** | Données nettoyées, typées, sans doublon | Une ligne par message (upsert) | `messages_silver`, `messages_scored` |
| **Gold** | Indicateurs prêts pour l'analyse | Petit, agrégé, lisible par le dashboard | `gold_spam_daily_sender`, `gold_model_metrics` |

## 3. Vocabulaire Hudi

| Terme | Définition simple | Dans notre projet |
|---|---|---|
| **Clé d'enregistrement** (record key) | Identifiant unique d'une ligne | `message_id` |
| **Champ de précombinaison** | Si deux lignes ont la même clé, celle avec la **plus grande valeur** de ce champ gagne | `ingest_ts` |
| **Chemin de partition** | Dossier de rangement des fichiers (accélère les lectures filtrées) | `event_date` |
| **Upsert** | Si la clé existe : on met à jour ; sinon : on insère | Écriture de Silver sans doublon |
| **Copy-on-Write (COW)** | À chaque mise à jour, les fichiers Parquet concernés sont **réécrits**. Lecture simple et rapide, écriture un peu plus lourde | Choix proposé (voir ADR-0001) |
| **Merge-on-Read (MoR)** | Les changements sont écrits dans des fichiers « log », **fusionnés à la lecture** ou par compaction. Écriture rapide, lecture plus complexe | Alternative |
| **Timeline / commit** | Chaque écriture crée un « instant » daté dans l'historique de la table | Base du time travel |
| **Time travel** | Relire la table **telle qu'elle était** à un instant passé | Démonstration de soutenance |
| **Requête incrémentale** | Lire seulement ce qui a changé depuis un instant donné | Démonstration de soutenance |

## 4. Pourquoi un Lakehouse pour notre filtre anti-spam ?

- Le flux est continu : Kafka envoie des messages en permanence, on veut des **mises à jour** (upsert) sans doublon.
- Bronze garde la donnée brute : si on change le nettoyage, on **rejoue** depuis Bronze.
- Le time travel permet de retrouver l'état de Silver avant un traitement douteux.
- Le Gold, petit et agrégé, alimente le dashboard sans relire tous les messages.

## 5. À retenir pour l'oral

> « Bronze garde la vérité brute, Silver la rend propre et unique, Gold la rend utile. Hudi donne au lac de fichiers
> les mises à jour et l'historique d'une base de données. »
