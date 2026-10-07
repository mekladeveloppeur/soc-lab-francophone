# Architecture du laboratoire

## Flux de démonstration

```text
Journaux JSONL fictifs
        |
        +--> tools/detect_bruteforce.py --> alerte JSON sur stdout
        |
        +--> detections/wazuh/local-rules.xml (exemple à tester en lab)
        |
        +--> detections/sentinel/auth-failures.kql (exemple KQL à adapter)
                         |
                         v
          Triage -> collecte de preuves -> réponse -> remédiation
```

## Contrat d'événement

Chaque ligne de `data/auth-events.jsonl` est un objet indépendant contenant :

| Champ | Sens | Exemple fictif |
| --- | --- | --- |
| `event_id` | Identifiant d'événement de démonstration | `LAB-AUTH-001` |
| `timestamp` | Date ISO 8601 avec fuseau | `2026-10-06T15:02:10Z` |
| `username` | Compte fictif | `agent.demo` |
| `source_ip` | Adresse réservée à la documentation | `203.0.113.77` |
| `outcome` | Résultat normalisé | `failure` |
| `auth_method` | Mécanisme de connexion de la simulation | `password` |
| `asset` | Hôte fictif | `auth-lab-01` |

## Limites techniques

- Le détecteur Python lit le fichier fourni et n'effectue aucune connexion réseau.
- La règle générique compte les échecs depuis une même IP ; elle ne prouve pas la compromission d'un compte.
- La correspondance MITRE ATT&CK reste au niveau **T1110**. Les données ne suffisent pas à distinguer sûrement password guessing, password spraying et credential stuffing.
- Les exemples SIEM sont des points de départ. Le décodage, les noms de champs, les tables disponibles et les seuils doivent être validés dans un environnement de test autorisé.
- Aucun service, base de données, compte ou système de client n'est nécessaire au fonctionnement de ce dépôt.
