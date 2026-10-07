# Cas d'école : revue de sécurité OWASP

**Application :** `portail-demo.example.test` (fictive)  
**Statut :** exercice documentaire ; aucune application n'a été scannée ou testée  
**But :** démontrer comment transformer une observation simulée en recommandation exploitable.

## Constat A — contrôle d'accès à confirmer

- **Référence :** OWASP Top 10 2021 A01 — Broken Access Control.
- **Observation simulée :** une route `/admin` n'applique pas de contrôle d'autorisation au niveau de l'objet dans le code fictif.
- **Risque :** accès non autorisé à des fonctions ou données si l'hypothèse se confirmait dans une application réelle.
- **Preuve de laboratoire :** note de revue du pseudo-code ; aucun appel réseau et aucune donnée réelle.
- **Remédiation :** appliquer une autorisation côté serveur pour chaque opération sensible, refuser par défaut, vérifier la propriété au niveau de l'objet, ajouter des tests d'accès positif et négatif.
- **Validation de correction :** tests automatisés pour les rôles autorisés et non autorisés ; revue des journaux d'audit.

## Constat B — requête de données à paramétrer

- **Référence :** OWASP Top 10 2021 A03 — Injection.
- **Observation simulée :** le pseudo-code de démonstration construit une requête à partir d'une valeur non fiable.
- **Risque :** manipulation de la requête si un problème équivalent existait dans une application.
- **Preuve de laboratoire :** extrait fictif uniquement ; aucun payload d'exploitation n'est fourni.
- **Remédiation :** requêtes paramétrées, validation selon le type métier, privilèges minimaux pour le compte de base de données.
- **Validation de correction :** tests de validation et revue du code confirmant l'absence de concaténation de valeurs non fiables.

## Constat C — protection de l'authentification à vérifier

- **Référence :** OWASP Top 10 2021 A07 — Identification and Authentication Failures.
- **Observation simulée :** le scénario de revue ne définit ni limitation d'essais ni contrôle MFA pour une opération à risque.
- **Risque :** exposition accrue aux tentatives d'accès automatisées.
- **Remédiation :** limitation adaptative, MFA appropriée au risque, récupération de compte sécurisée et alertes sur les changements sensibles.
- **Validation de correction :** tests contrôlés en laboratoire, vérification de l'expérience de récupération et revue des alertes.

## Constat D — traçabilité de sécurité à améliorer

- **Référence :** OWASP Top 10 2021 A09 — Security Logging and Monitoring Failures.
- **Observation simulée :** le cas ne définit pas d'événements auditables pour les modifications administratives.
- **Risque :** détection et investigation plus difficiles en cas d'incident.
- **Remédiation :** journaliser les actions sensibles avec identité, résultat, horodatage et corrélation ; protéger l'accès et la conservation des journaux ; éviter d'y stocker des secrets.
- **Validation de correction :** déclencher un événement de test approuvé et vérifier sa réception, sa recherche et sa rétention.

## Priorisation indicative

Prioriser selon exposition, impact métier, facilité d'exploitation démontrée dans un environnement autorisé, mesures compensatoires et fiabilité des preuves. Les niveaux de sévérité doivent être recalculés pour l'application réelle ; ce document n'attribue pas de note CVSS à un système réel.
