# Documentation du Data Lake et du Lakehouse (E2)

Propriétaire : **Étudiant 2 (E2)** · Tâche de la feuille de route : **E2-01** (phase P0)

| Document | Contenu |
|---|---|
| [notions.md](notions.md) | Data Lake, entrepôt, Lakehouse, Bronze / Silver / Gold, vocabulaire Hudi |
| [arborescence.md](arborescence.md) | Buckets MinIO, conventions de nommage, partitionnement, schéma des zones |
| [parcours_message.md](parcours_message.md) | Le parcours complet d'un message, de Kafka au Gold |
| [../adr/0001-type-tables-hudi.md](../adr/0001-type-tables-hudi.md) | Choix Copy-on-Write ou Merge-on-Read (proposition à valider en P2) |

Les noms de tables et leurs colonnes sont dans [../contrat_interface.md](../contrat_interface.md) : **source de vérité**.

## État d'avancement (E2)

- [x] E2-01 Notions comprises et documentées
- [x] E2-01 Arborescence du lake conçue
- [ ] E2-01 Validée par E3 et E4 (relecture de la pull request finale ou message dans le groupe)
- [ ] E2-02 MinIO dans Compose (phase P1)
