# Runbook : rafale d'échecs d'authentification

**Type :** exercice de laboratoire uniquement  
**Priorité initiale :** élevée si un succès suit une rafale, sinon à confirmer par le contexte  
**Données :** événements fictifs de `data/auth-events.jsonl`

## 1. Valider l'alerte

1. Confirmer la période, le seuil, le nombre de comptes visés et l'adresse source.
2. Vérifier que les événements sont bien des échecs d'authentification et ne sont pas des doublons.
3. Rechercher un succès ultérieur depuis la même source ou visant les mêmes comptes.
4. Comparer à une fenêtre de référence documentée : VPN, tâches automatisées et tests autorisés peuvent produire du bruit.
5. Consigner les identifiants des événements et conserver les horodatages en UTC.

## 2. Délimiter l'incident

- Identifier les comptes, hôtes et services concernés à partir des journaux autorisés.
- Rechercher d'autres signaux associés : changements de facteurs MFA, réinitialisations, sessions inhabituelles ou élévations de privilèges.
- Distinguer une tentative bloquée d'un accès confirmé ; ne pas conclure sur la seule base du volume d'échecs.
- Évaluer le périmètre et le niveau de confiance avant l'escalade.

## 3. Confinement — uniquement avec autorisation

- Suivre le processus interne d'approbation avant de bloquer une IP ou de désactiver un compte.
- En cas de succès suspect confirmé, coordonner la révocation des sessions et la rotation des secrets avec le propriétaire du système.
- Préserver d'abord les preuves nécessaires et noter l'heure, l'approbateur et l'effet attendu de chaque action.
- Ne jamais exécuter ces actions sur un système réel depuis ce dépôt.

## 4. Rétablissement et clôture

- Confirmer avec le propriétaire du service que l'accès légitime fonctionne après le confinement.
- Rechercher une reprise de l'activité pendant une période définie par l'équipe responsable.
- Enregistrer la chronologie, les preuves, les décisions, les faux positifs et les actions de remédiation.
- Créer un suivi mesurable : responsable, échéance, contrôle à vérifier.

## Fiche d'investigation

```text
ID de l'alerte :
Analyste / heure UTC :
Source et fenêtre :
Comptes concernés :
Échecs / succès observés :
Preuves conservées (IDs, emplacement autorisé) :
Hypothèses et niveau de confiance :
Décision / approbateur :
Actions et résultat :
Motif de clôture / suivi :
```

## Référentiel

- MITRE ATT&CK : T1110 — Brute Force.
- Les contrôles de limitation, MFA, verrouillage adaptatif et journalisation doivent être choisis selon le contexte, le risque de déni de service et les exigences de l'organisation.
