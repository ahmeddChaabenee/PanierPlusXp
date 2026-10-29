\# PanierPlus — Product Backlog



\## Objectif



Développer une mini-application Python de gestion de panier d'achat afin de comparer une approche classique de développement avec Extreme Programming (XP).



Les deux expériences doivent utiliser :

\- Le même code initial.

\- Le même backlog.

\- Les mêmes critères d'acceptation.

\- La même demande de changement CR1.

\- Les mêmes outils de validation.



\## Environnement technique



\- Python 3.12

\- pytest

\- pytest-cov

\- Ruff

\- GitHub Actions



\## S1 — Gestion du panier



\*\*Description :\*\* En tant que client, je veux gérer les articles de mon panier.



Critères d'acceptation :

\- Ajouter un article avec son nom, sa catégorie, son prix et sa quantité.

\- Refuser une quantité négative ou nulle.

\- Modifier la quantité d'un article.

\- Retirer un article.

\- Calculer le sous-total des articles.



\## S2 — Code promotionnel PROMO10



\*\*Description :\*\* En tant que client, je veux appliquer une réduction promotionnelle.



Critères d'acceptation :

\- Le code PROMO10 applique une réduction de 10 %.

\- Un code inconnu ne donne aucune réduction.

\- Le montant final ne peut pas être négatif.



\## S3 — Calcul de la TVA



\*\*Description :\*\* En tant que client, je veux que la TVA soit calculée selon la catégorie du produit.



Critères d'acceptation :

\- Chaque catégorie possède un taux de TVA défini.

\- La TVA est calculée à partir du montant concerné.

\- Le total TTC est calculé correctement.



Les taux utilisés doivent être définis et identiques dans les deux expériences.



\## S4 — Offre « 3 achetés, 1 offert »



\*\*Description :\*\* En tant que client, je veux bénéficier d'une offre lorsqu'elle est applicable.



Critères d'acceptation :

\- Pour quatre unités éligibles, une unité est offerte.

\- Le nombre d'unités offertes dépend de la quantité achetée.

\- Le montant de la réduction est calculé correctement.



\## S5 — Cumul et priorité des réductions



\*\*Description :\*\* En tant que responsable produit, je veux que les règles de réduction soient appliquées de manière cohérente.



Critères d'acceptation :

\- Les règles de cumul sont explicites.

\- L'ordre d'application des réductions est défini.

\- Un plafond de réduction est respecté.

\- Le montant final ne peut pas être négatif.



\## CR1 — Demande de changement commune



\*\*Demande :\*\* Le code promotionnel PROMO10 ne doit plus fonctionner pour les produits de catégorie LIVRE.



Critères d'acceptation :

\- PROMO10 ne réduit pas le prix des produits LIVRE.

\- PROMO10 reste applicable aux catégories éligibles.

\- Les autres règles de calcul ne sont pas modifiées.

\- Les tests existants continuent de passer.



\## Règle de comparaison



Les expériences classique et XP doivent traiter S1 à S5, puis CR1, dans les mêmes conditions.



Les temps, défauts, résultats de tests et événements CI doivent être mesurés réellement. Aucune donnée simulée ne doit être présentée comme une mesure réelle.





## Règles métier communes aux deux expériences



\### Prix et quantités

\- Les prix sont exprimés en euros.

\- Un prix doit être positif ou nul.

\- Une quantité doit être un entier strictement positif.

\- Les calculs monétaires sont arrondis à deux décimales.

\- Les calculs utilisent Decimal pour éviter les imprécisions classiques des nombres flottants.



\### Catégories et TVA

Pour cette expérience pédagogique, les taux sont fictifs et servent uniquement à rendre les calculs reproductibles :

\- LIVRE : 5,5 %

\- STANDARD : 20 %



La TVA est calculée après application des réductions. Le montant TTC est égal au montant HT après réduction, augmenté de la TVA applicable.



\### Code promotionnel PROMO10

\- PROMO10 applique une réduction de 10 % sur les produits éligibles.

\- Avant CR1, toutes les catégories sont éligibles.

\- Après CR1, les produits de catégorie LIVRE ne bénéficient plus de cette réduction.

\- Un code inconnu ne donne aucune réduction.

\- La réduction ne peut pas dépasser le montant éligible.



\### Offre « 3 achetés, 1 offert »

\- L'offre s'applique aux produits explicitement marqués comme éligibles.

\- Chaque groupe de quatre unités donne droit à une unité offerte.

\- Le prix unitaire le plus bas du groupe est utilisé pour calculer la réduction.

\- L'offre ne s'applique pas automatiquement à tous les produits.



\### Cumul des réductions

\- L'offre « 3 achetés, 1 offert » est calculée avant PROMO10.

\- PROMO10 est calculé sur le montant restant des produits éligibles.

\- La somme des réductions ne peut pas dépasser le sous-total HT.

\- La TVA est calculée sur le montant HT après réductions.



\### Demande de changement CR1

La modification CR1 interdit PROMO10 pour la catégorie LIVRE sans modifier les autres catégories ni les règles de TVA et d'offre.



\### Comparabilité

Ces règles sont communes aux deux branches. Toute modification de règle doit être documentée et appliquée aux deux expériences.

