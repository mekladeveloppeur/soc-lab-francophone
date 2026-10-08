# Étude de cas — échecs d'authentification et succès corrélé

> **Nature :** simulation pédagogique sur des journaux synthétiques. Ce cas ne décrit pas une mission client, une opération réelle ni un travail réalisé pour l'ANC de Djibouti.

## Résumé de l'exercice

Le laboratoire analyse sept événements d'authentification sur `auth-lab-01`. Une même adresse d'exemple produit cinq échecs visant quatre comptes en deux minutes et cinquante-quatre secondes. Deux minutes et vingt-sept secondes après le dernier échec, le compte `support.demo` réussit une authentification depuis cette source.

La règle `SOC-AUTH-001` détecte la rafale de cinq échecs dans une fenêtre de dix minutes. Le succès corrélé est ajouté comme élément de contexte et augmente la priorité de triage, sans constituer une preuve suffisante de compromission.

## Éléments de preuve

| Horodatage UTC | Événements | Résultat | Compte(s) |
| --- | --- | --- | --- |
| 15:02:10–15:05:04 | `LAB-AUTH-001` à `LAB-AUTH-005` | 5 échecs | `agent.demo`, `support.demo`, `finance.demo`, `admin.demo` |
| 15:07:31 | `LAB-AUTH-006` | Succès après la rafale | `support.demo` |
| 15:09:15 | `LAB-AUTH-007` | Succès depuis une autre IP d'exemple | `analyst.demo` |

Les adresses `203.0.113.77` et `198.51.100.24` font partie des plages réservées à la documentation. Elles ne représentent ni des postes ni des indicateurs réels.

## Hypothèses et limites

- **Hypothèse à examiner :** tentative de force brute multi-comptes ou autre abus d'identifiants.
- **Technique de référence :** MITRE ATT&CK T1110 — Brute Force. Les événements ne permettent pas de confirmer une sous-technique telle que le password spraying.
- **Ce qui est établi dans le jeu de données :** cinq résultats d'échec, quatre comptes visés et un succès ultérieur depuis la même adresse fictive.
- **Ce qui n'est pas établi :** l'intention, l'identité de l'opérateur, la légitimité du succès, l'utilisation de MFA, l'appareil, la session ou un impact métier.
- Une tâche automatisée, un test autorisé, une adresse partagée ou une erreur utilisateur peuvent également produire des échecs. Le contexte réel doit être vérifié auprès des propriétaires de systèmes autorisés.

## Plan de triage pédagogique

1. **Valider le signal :** contrôler le seuil, la fenêtre, l'ordre chronologique et les identifiants de preuve. Comparer les événements à une référence autorisée (VPN, NAT, maintenance ou tests prévus).
2. **Valider le succès :** confirmer auprès du propriétaire du compte `support.demo` si l'accès était attendu ; consulter, si disponibles, les événements MFA, l'appareil et les informations de session dans une source autorisée.
3. **Délimiter :** rechercher des événements associés aux comptes et à la session, notamment changements de facteurs, réinitialisations ou modifications de privilèges.
4. **Décider :** qualifier l'alerte selon les preuves et le niveau de confiance. Ne pas conclure à une compromission sur le seul volume d'échecs.
5. **Répondre si l'accès suspect est confirmé :** appliquer la procédure approuvée par l'organisation pour préserver les preuves, révoquer une session ou renouveler des identifiants. Cette démonstration n'exécute aucune action sur un système.

## Reproduire

Depuis le dossier `github/` du dépôt :

```bash
python3 tools/detect_bruteforce.py data/auth-events.jsonl
python3 -m unittest discover -s tests -v
```

Les exemples Wazuh et Microsoft Sentinel sont des modèles à valider dans un laboratoire autorisé. Le site ne se connecte à aucun SIEM et les changements d'état de triage restent locaux à la session.

## Présenter le projet

> « J'ai construit un laboratoire SOC pédagogique qui analyse des événements d'authentification synthétiques. La règle détecte cinq échecs dans une fenêtre de dix minutes, puis rattache un succès ultérieur comme élément de contexte. Je montre les preuves, les limites de la conclusion et les vérifications d'un analyste avant toute réponse. Ce n'est ni une alerte de production ni une mission réalisée pour une organisation. »
