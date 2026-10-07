# SOC Lab Francophone

Laboratoire pédagogique en français consacré à la surveillance SOC, au triage SIEM, à l'investigation et à la remédiation d'un audit OWASP.

> **Périmètre de sécurité :** tous les noms, adresses IP, journaux, alertes et constats de ce dépôt sont fictifs. Ce laboratoire n'est relié à aucun réseau client et ne contient aucune donnée issue d'une mission réelle. Les scénarios servent à démontrer une méthode, pas à prétendre qu'ils ont été exécutés chez un client.

## Pourquoi ce projet ?

Le CV et l'attestation mentionnent des compétences et expériences en surveillance SIEM avec Wazuh et Microsoft Sentinel, analyse de journaux, triage d'alertes, réponse aux incidents, MITRE ATT&CK et audit OWASP. Ce dépôt rassemble ces thèmes dans **un projet de portfolio** composé de démonstrations sûres et reproductibles.

## Trois modules complémentaires

### 1. Détection SIEM et triage SOC

- Journaux d'authentification entièrement synthétiques dans `data/auth-events.jsonl`.
- Détecteur Python sans dépendance externe : seuil de cinq échecs d'authentification depuis une même adresse IP dans une fenêtre de dix minutes.
- Exemple de règle Wazuh et requête Microsoft Sentinel dans `detections/`.
- Alertes mappées à MITRE ATT&CK **T1110 — Brute Force**. Le journal seul ne permet pas de conclure à une sous-technique plus précise.

### 2. Investigation et réponse aux incidents

- Scénario fictif d'abus d'identifiants.
- Guide de réponse structuré : validation, collecte des preuves, délimitation, confinement, rétablissement et retour d'expérience.
- Fiche d'investigation et critères d'escalade dans `docs/runbooks/credential-abuse.md`.

### 3. Audit applicatif OWASP et remédiation

- Cas d'école non connecté à une application réelle, avec constats illustratifs, impact, preuves simulées et recommandations.
- Contrôles alignés sur des catégories OWASP Top 10 (2021) et principes ISO 27001.
- Aucun test d'intrusion réel ni payload d'exploitation n'est inclus.

## Démarrer le détecteur local

Prérequis : Python 3.10 ou ultérieur. Le détecteur utilise uniquement la bibliothèque standard.

```bash
python3 tools/detect_bruteforce.py data/auth-events.jsonl
python3 -m unittest discover -s tests -v
```

Le premier lancement affiche une alerte JSON de démonstration. Pour changer le seuil ou la fenêtre :

```bash
python3 tools/detect_bruteforce.py data/auth-events.jsonl --threshold 4 --window-minutes 15
```

La sortie ne modifie aucun système : le programme lit un fichier local et écrit les alertes sur la sortie standard.

## Arborescence

```text
data/                       Journaux fictifs au format JSON Lines
detections/
  sentinel/                  Exemple de requête KQL
  wazuh/                     Règle XML pédagogique
docs/
  architecture.md            Flux de données et limites du laboratoire
  runbooks/                  Procédure de réponse aux incidents
  audit/                     Exemple de constats OWASP et remédiations
tools/                       Détecteur Python en lecture seule
tests/                       Tests unitaires sur données synthétiques
```

## Limites et usage responsable

- N'importez pas de journaux clients, de données personnelles, de secrets ou d'adresses IP réelles.
- N'exécutez pas de tests sur un système sans autorisation écrite et un périmètre défini.
- Les fichiers Wazuh et KQL sont des exemples à adapter et valider dans un environnement de laboratoire autorisé.
- Une alerte de brute force constitue un signal à investiguer, pas une preuve d'intrusion.
- Les cas OWASP sont des exercices de documentation ; ils ne constituent pas un rapport d'audit réel.

## Licence

Les éléments originaux de ce laboratoire sont distribués sous licence MIT. Les noms de produits et les références à MITRE ATT&CK, OWASP, Wazuh et Microsoft Sentinel identifient des outils ou référentiels tiers et n'impliquent aucune approbation de leur part.
