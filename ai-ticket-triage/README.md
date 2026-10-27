# Triage de tickets TI assisté par IA

Petit outil Python qui lit des tickets de soutien (CSV), puis pour chacun :
1. classe le ticket dans une catégorie (compte, réseau, impression, courriel, poste, logiciel, sécurité) ;
2. fixe une priorité (P1 à P4) et indique s'il faut **escalader** ;
3. retrouve dans `kb.json` l'article de base de connaissances correspondant et en propose les étapes ;
4. rédige une réponse à l'utilisateur.

## Deux modes
- **Règles (défaut)** : mots-clés et priorités, fonctionne hors ligne.
- **IA (`--ai`)** : un modèle de langage classe le ticket et rédige la réponse. La sortie est **validée** (catégorie et priorité doivent être des valeurs connues) ; sinon l'outil retombe sur les règles. Il ne demande jamais de mot de passe.

## Usage
```bash
python3 triage.py                         # tickets d'exemple
python3 triage.py mes_tickets.csv --out rapport.csv
ANTHROPIC_API_KEY=... python3 triage.py --ai
python3 -m pytest tests
```

## Limites connues (à documenter honnêtement)
- Le mode règles ne comprend pas le contexte (ex. un ticket « Autre » peut cacher une vraie panne).
- Le mode IA peut se tromper ou inventer ; un humain valide toujours avant d'envoyer la réponse.
- Les données d'exemple sont fictives. N'envoie jamais de données confidentielles à un service externe.

## Idées d'amélioration
- Recherche sémantique (embeddings) dans la base de connaissances.
- Interface web simple (Flask) pour coller un ticket.
- Mesurer la précision règles vs IA sur 50 tickets étiquetés à la main.
