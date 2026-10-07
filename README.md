# Abdoulkader Abdila Mohamed — Analyste SOC

Portfolio professionnel en français et dépôt de démonstrations techniques.

**Portfolio en ligne :** https://mekladeveloppeur.github.io/soc-lab-francophone/

Ce dépôt distingue l’expérience professionnelle attestée des exercices techniques publiés. Les exemples du code sont synthétiques ou fictifs ; ils ne constituent pas des preuves de travaux réalisés pour un client.

## Expérience professionnelle

**Djib Data-AI Consulting EURL · Djibouti**

### Supervision et détection des menaces · 1 septembre 2024 – 28 février 2025

- Mise en œuvre d’une architecture de surveillance avec Wazuh et Microsoft Sentinel.
- Configuration de règles de détection et d’alerte.
- Analyse de journaux système et réseau.
- Définition de procédures de réponse aux incidents et formation d’équipes techniques.

### Audit de sécurité applicative · 1 mars 2025 – 30 juin 2025

- Tests d’intrusion et analyse de vulnérabilités applicatives et d’infrastructure.
- Évaluation selon OWASP et ISO 27001.
- Rédaction d’un rapport d’audit et de recommandations de remédiation.

L’attestation a été délivrée le 1 février 2026 ; les missions qu’elle décrit se sont terminées le 30 juin 2025. Aucun emploi après cette date n’est revendiqué ici.

## Démonstrations techniques du dépôt

- **Détection SOC :** événements synthétiques, script Python de détection de tentatives par force brute, exemple de règle Wazuh et requête KQL pour Sentinel.
- **Réponse à incident :** scénario fictif et runbook pédagogique.
- **Sécurité applicative :** étude OWASP fictive, sans test sur une cible réelle.

Ces ressources sont des démonstrations indépendantes. Elles ne proviennent pas des missions professionnelles et ne reproduisent aucun journal, constat, rapport ou environnement client.

## Lancer les exemples

Prérequis : Python 3.10 ou ultérieur.

```bash
python3 tools/detect_bruteforce.py data/auth-events.jsonl
python3 -m unittest discover -s tests -v
```

Le détecteur traite uniquement le fichier synthétique fourni et écrit sa sortie dans le terminal. Il ne se connecte à aucun système.

## Confidentialité et usage responsable

- Les clients, plateformes, cibles, données et constats sensibles ne sont pas publiés.
- Les journaux du dépôt sont synthétiques ; n’y ajoutez pas de données personnelles, de secrets ni de journaux clients.
- N’exécutez des tests de sécurité que sur des systèmes pour lesquels vous avez une autorisation et un périmètre défini.
- Les exemples Wazuh et Sentinel doivent être adaptés et validés dans un environnement autorisé.

## Licence

Les exemples originaux sont distribués sous licence MIT. Les marques Wazuh, Microsoft Sentinel, MITRE ATT&CK, OWASP et ISO appartiennent à leurs détenteurs respectifs.
