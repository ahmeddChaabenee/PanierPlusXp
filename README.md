\# PanierPlus — Comparaison des méthodes de développement



\## Objectif



Ce projet compare deux approches de développement logiciel :



\- Approche classique

\- Extreme Programming (XP)



L'objectif est d'observer comment les pratiques de développement influencent la qualité du code, les tests, les défauts et la capacité à intégrer une demande de changement.



\## Application



PanierPlus est une mini-application Python de gestion de panier d'achat.



Fonctionnalités prévues :



\- S1 : gestion du panier

\- S2 : code promotionnel PROMO10

\- S3 : calcul de la TVA

\- S4 : offre « 3 achetés, 1 offert »

\- S5 : cumul et priorité des réductions



Une demande de changement commune, CR1, interdira ensuite l'utilisation de PROMO10 pour les produits de catégorie LIVRE.



\## Environnement technique



\- Python 3.12

\- pytest

\- pytest-cov

\- Ruff

\- Git

\- GitHub Actions



\## Organisation



\- `panierplus/` : code de l'application

\- `tests/` : tests automatisés

\- `docs/` : backlog, règles de qualité et journal des expériences

\- `.github/workflows/` : configuration de l'intégration continue



\## Protocole expérimental



Les deux expériences partent du même commit initial et utilisent le même backlog ainsi que les mêmes critères d'acceptation.



Les résultats seront mesurés pendant les expériences. Les données non mesurées seront identifiées comme telles.



\## État du projet



Préparation de l'environnement et définition du protocole expérimental.

