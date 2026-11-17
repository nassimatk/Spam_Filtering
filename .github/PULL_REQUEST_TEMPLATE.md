## Quoi ?
<!-- Résumé en 1-2 phrases. Lien avec la tâche : « Closes #12 » ou identifiant roadmap (ex. E3-05). -->

## Service concerné
- [ ] E1 producer/  - [ ] E2 lakehouse/  - [ ] E3 spark/  - [ ] E4 airflow/ + superset/  - [ ] commun

## Checklist « terminé »
- [ ] Le code fonctionne **dans Docker** (pas seulement sur ma machine)
- [ ] `docker compose config -q` passe ; pas de secret committé (`.env` ignoré)
- [ ] README / docs mis à jour (et `docs/contrat_interface.md` si un nom, un schéma ou un topic change)
- [ ] Les autres services impactés ont été prévenus (mentionner @ci-dessous)
- [ ] `make lint` et `make test` passent

## Comment tester
<!-- Commandes exactes : commandes de lancement, captures si utile -->
