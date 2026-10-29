\# Definition of Done — PanierPlus



\## Objectif



Définir les conditions minimales qu'une fonctionnalité doit respecter pour être considérée comme terminée.



Les critères fonctionnels et les exigences finales de qualité sont identiques pour les expériences classique et XP.



\## DoD commune — Version 1



Une fonctionnalité est terminée lorsque :



\- \[ ] Les critères d'acceptation sont respectés.

\- \[ ] Le code fonctionne avec Python 3.12.

\- \[ ] Les tests automatisés associés passent.

\- \[ ] Les tests de non-régression passent.

\- \[ ] Ruff ne signale aucune erreur.

\- \[ ] La CI est verte.

\- \[ ] Aucun défaut connu ne bloque le fonctionnement attendu.

\- \[ ] Les résultats et le temps consacré sont consignés dans le journal d'expérience.



\## Exigences de qualité supplémentaires — Version 2



Pour les changements réalisés après l'introduction de CR1, vérifier également :



\- \[ ] Les tests couvrent le nouveau comportement.

\- \[ ] Les tests sont exécutés avant la validation du changement.

\- \[ ] La couverture des lignes modifiées est d'au moins 85 %, lorsque la mesure est disponible.

\- \[ ] La couverture globale ne diminue pas.

\- \[ ] La CI reste verte.

\- \[ ] La modification est relue par un autre membre ou fait l'objet d'une revue de code.

\- \[ ] La branche de travail reste courte et les intégrations sont fréquentes.

\- \[ ] Les éventuelles dettes techniques sont documentées.



\## Application dans les deux expériences



\### Approche classique

Le développeur peut commencer par écrire le code puis ajouter les tests. Les mêmes critères de qualité finale doivent néanmoins être vérifiés.



\### Extreme Programming (XP)

Le développeur écrit d'abord un test qui échoue, implémente le minimum nécessaire pour le faire passer, puis refactorise. La programmation en binôme et l'intégration continue sont appliquées selon le protocole de l'expérience.



\## Règle importante



La Definition of Done ne doit pas être utilisée pour favoriser artificiellement une méthode. Les critères fonctionnels et les exigences finales sont communs. Les pratiques de développement sont celles que l'expérience cherche à comparer.

