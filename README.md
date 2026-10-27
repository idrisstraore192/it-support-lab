# Laboratoire de soutien TI + triage de tickets assisté par IA

Projet personnel de **Cheik Idriss Traoré** (diplômé en informatique et génie logiciel, UQAM 2026) pour démontrer des compétences de soutien TI de niveau 1 : diagnostic, documentation, support aux utilisateurs, et utilisation responsable de l'IA.

Tout est fictif : aucune donnée réelle d'utilisateur ou d'entreprise.

## Contenu

| Dossier | Description |
|---|---|
| `docs/lab-guide.md` | Guide du laboratoire : machine virtuelle Windows, comptes, réseau, Microsoft 365, Active Directory (par phases, avec cases à cocher). |
| `docs/incidents/` | Journal d'incidents : un fichier par panne reproduite et résolue (modèle fourni). |
| `ai-ticket-triage/` | Outil Python qui classe des tickets de soutien, fixe la priorité, propose des étapes de résolution à partir d'une base de connaissances et rédige une réponse (avec ou sans IA). |

## Démarrage rapide (outil de triage)

```bash
cd ai-ticket-triage
python3 triage.py                     # mode règles, hors ligne
python3 -m pytest tests               # tests
# Optionnel : mode IA
pip install -r requirements.txt
export ANTHROPIC_API_KEY=...          # ne jamais le mettre dans Git
python3 triage.py --ai
```

## Ce que j'ai appris / démontré (à compléter au fur et à mesure)

- [ ] Créer et configurer une VM Windows
- [ ] Gérer des comptes utilisateurs et des mots de passe
- [ ] Diagnostiquer des problèmes réseau de base (ipconfig, ping, nslookup)
- [ ] Documenter 10 incidents selon un modèle
- [ ] Automatiser du triage avec Python et valider les sorties d'une IA

*Ne coche que ce que tu as réellement fait.*
