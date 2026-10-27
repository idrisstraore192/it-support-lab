# Guide du laboratoire de soutien TI

Coche chaque case seulement après l'avoir réalisée, et note la date dans ton journal. Prends des captures d'écran (sans information personnelle) pour chaque phase.

> Matériel : un Mac (Apple silicon) a des contraintes. Les VM x86 y sont émulées et lentes. Si tu bloques, dis-le-moi et on adapte (par exemple Windows 11 ARM, ou un autre poste).

## Phase 0 — Préparation (30 min)
- [ ] Créer un dépôt GitHub public `it-support-lab` et y copier ce dossier.
- [ ] Créer un fichier `docs/journal.md` : une ligne par séance (date, durée, ce que j'ai fait).
- [ ] Vérifier l'espace disque libre (prévoir 60 Go).

## Phase 1 — Poste Windows virtuel (2-3 h)
Outil : UTM (Mac) ou VirtualBox (PC).
- [ ] Installer l'hyperviseur.
- [ ] Obtenir l'ISO Windows 11 (version ARM64 pour un Mac Apple silicon) sur le site officiel de Microsoft.
- [ ] Créer la VM (4 Go RAM, 2 cœurs, 50 Go) et installer Windows.
- [ ] Créer un compte administrateur et 2 comptes standard (`utilisateur1`, `utilisateur2`).
- [ ] Prendre un instantané (snapshot) « install propre ».

## Phase 2 — Opérations de base d'un technicien (2 h)
- [ ] Réinitialiser le mot de passe d'un compte local et forcer le changement à la prochaine ouverture.
- [ ] Créer un dossier partagé avec permissions différentes par utilisateur.
- [ ] Mettre en place une imprimante virtuelle (PDF) et vider la file d'attente.
- [ ] Utiliser Gestionnaire des tâches, Observateur d'événements, Services, Gestion des disques.
- [ ] Réseau : `ipconfig /all`, `ping`, `nslookup`, `tracert` ; noter le résultat de chacun.

## Phase 3 — Microsoft 365 (2-3 h)
- [ ] Obtenir un environnement d'essai ou de développement Microsoft 365 (vérifie sur le site de Microsoft ce qui est offert actuellement ; ne saisis pas de carte bancaire sans avoir lu les conditions).
- [ ] Créer 3 utilisateurs, attribuer des licences, réinitialiser un mot de passe.
- [ ] Configurer l'authentification multifacteur sur un compte de test.
- [ ] Créer un groupe, une boîte aux lettres partagée, un site Teams/SharePoint de test.

## Phase 4 — Active Directory (3-4 h, optionnel selon le matériel)
- [ ] Installer Windows Server (version d'évaluation) dans une deuxième VM.
- [ ] Promouvoir le serveur en contrôleur de domaine (domaine fictif `lab.local`).
- [ ] Créer des unités d'organisation, utilisateurs et groupes ; joindre le poste Windows au domaine.
- [ ] Appliquer une stratégie de groupe simple (ex. fond d'écran ou verrouillage d'écran).

## Phase 5 — 10 incidents documentés (en continu)
Reproduis puis résous chaque panne, et remplis `docs/incidents/_modele.md` :
1. Mot de passe oublié / compte verrouillé
2. Pas d'accès Internet (mauvaise IP / DNS)
3. Dossier partagé inaccessible (permissions)
4. Imprimante bloquée
5. Ordinateur lent (démarrage, disque plein)
6. Application qui plante
7. Profil Outlook / compte Microsoft 365 qui ne se synchronise pas
8. Poste qui ne joint plus le domaine
9. Mise à jour Windows bloquée
10. Courriel d'hameçonnage simulé (procédure de signalement)

## Phase 6 — Projet IA : triage de tickets
Voir `ai-ticket-triage/`. Objectifs : lancer l'outil, ajouter 10 tickets de ton journal d'incidents, écrire 3 nouveaux articles dans `kb.json`, activer le mode IA avec ta propre clé, comparer les résultats des règles et de l'IA, et documenter les erreurs de l'IA.

## Règles
- Aucune donnée réelle, aucun mot de passe réel dans le dépôt.
- Une clé API ne va jamais dans Git (utilise une variable d'environnement et un `.gitignore`).
