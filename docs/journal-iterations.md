\# Journal des expériences — PanierPlus



\## Informations générales



Version de Python :

Membres de l'équipe :

Date de début :

Date de fin :

Commit initial commun :



\## Expérience A — Approche classique



\### S1 — Gestion du panier

Date :

Durée :

Défauts rencontrés :

Remarques :



\### S2 — Code promotionnel PROMO10

Date :

Durée :

Défauts rencontrés :

Remarques :



\### S3 — Calcul de la TVA

Date :

Durée :

Défauts rencontrés :

Remarques :



\### S4 — Offre « 3 achetés, 1 offert »

Date :

Durée :

Défauts rencontrés :

Remarques :



\### S5 — Cumul et priorité des réductions

Date :

Durée :

Défauts rencontrés :

Remarques :



\### CR1 — Modification du code promotionnel

Date :

Durée :

Défauts rencontrés :

Temps nécessaire pour corriger les problèmes :

Remarques :



\## Expérience B — Extreme Programming (XP)



\### S1 — Gestion du panier

Date :

Durée :

Défauts rencontrés :

Remarques :



\### S2 — Code promotionnel PROMO10

Date :

Durée :

Défauts rencontrés :

Remarques :



\### S3 — Calcul de la TVA

Date :

Durée :

Défauts rencontrés :

Remarques :



\### S4 — Offre « 3 achetés, 1 offert »

Date :

Durée :

Défauts rencontrés :

Remarques :





\### S5 — Cumul et priorité des réductions

Date : 29/10/2026

Durée : non mesurée

Défauts rencontrés :

\- Deux tests ont échoué car PROMO10 était calculé sur le sous-total complet au lieu du montant restant après l'offre.

\- Une erreur d'indentation a empêché la collecte des tests ; aucun test n'a été exécuté pendant cet incident.

\- Les durées de détection et de correction ne sont pas mesurées.

Remarques :

\- Ordre appliqué : offre « 3 achetés, 1 offert », puis PROMO10, puis calcul de la TVA.

\- 25 tests réussis après correction.

\- Couverture mesurée avant l'ajout du dernier test : 90 %.

\- Ruff : aucune erreur après correction du formatage.

\- Commit : a45a3da.

\- Le temps de correction n'a pas été mesuré.





\### CR1 — Modification du code promotionnel

Date :

Durée :

Défauts rencontrés :

Temps nécessaire pour corriger les problèmes :

Remarques :



\## Résultats finaux



\### Approche classique

\- Nombre de fonctionnalités terminées :

\- Durée totale de développement :

\- Temps nécessaire pour CR1 :

\- Nombre total de défauts :

\- Nombre de défauts détectés tardivement :

\- Temps total de correction :

\- Nombre d'échecs de CI :

\- Couverture des tests :



\### Extreme Programming (XP)

\- Nombre de fonctionnalités terminées :

\- Durée totale de développement :

\- Temps nécessaire pour CR1 :

\- Nombre total de défauts :

\- Nombre de défauts détectés tardivement :

\- Temps total de correction :

\- Nombre d'échecs de CI :

\- Couverture des tests :



\## Conclusion



Résultats observés :

Différences entre les deux approches :

Limites de l'expérience :



Remarque : toutes les valeurs doivent être mesurées pendant les expériences. Si une donnée n'est pas disponible, indiquer « non mesurée ».

