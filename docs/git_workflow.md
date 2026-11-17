# Workflow Git

Le suivi des contributions compte pour **40 % de la note individuelle** : le jury lit l'historique.

## Branches
- `main` : toujours démarrable (`make up`). **Protégée** : pas de push direct, pull request obligatoire.
- `develop` (optionnelle) : intégration entre phases.
- Branches de travail : `e1/producteur-kafka`, `e2/hudi-silver`, `e3/train-model`, `e4/dag-qualite`… (préfixe = étudiant).

## Commits
- Petits et fréquents, **sous son propre compte GitHub**.
- Message préfixé par la couche : `[kafka] ajoute le producteur`, `[hudi] upsert messages_silver`, `[spark] train_model`,
  `[airflow] DAG qualité`, `[superset] graphique top expéditeurs`, `[docs] …`, `[infra] …`.

## Pull requests
1. Ouvrir une PR vers `main` (modèle fourni), la relier à l'issue / à l'identifiant roadmap (E3-05…).
2. Relecture par **un autre membre** (CODEOWNERS la demande automatiquement).
3. CI verte (lint, tests, validation de `docker-compose.yml`).
4. Fusion « squash » ou « merge » ; supprimer la branche.

## Fichiers partagés (risque de conflit)
`docker-compose.yml`, `.env.example`, `docs/contrat_interface.md` : modifier **uniquement sa section**, PR courte,
prévenir l'équipe. Rebaser souvent : `git pull --rebase origin main`.

## Réglages GitHub à faire une fois (par le créateur du dépôt)
- Settings → Branches → règle de protection sur `main` (PR + 1 relecture + CI).
- Settings → Collaborators : ajouter les 3 autres membres ; remplacer les `@pseudo-eN` de `.github/CODEOWNERS`.
- Projects : tableau Kanban avec les tâches E1-01… du document de feuille de route.
