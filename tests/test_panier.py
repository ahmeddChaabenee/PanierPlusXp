
import pytest

from panierplus.panier import Article, Panier, calculer_sous_total


def test_calculer_sous_total():
    assert calculer_sous_total(10.0, 3) == 30.0


def test_calculer_sous_total_avec_decimales():
    assert calculer_sous_total(12.50, 2) == 25.00


def test_refuser_prix_negatif():
    with pytest.raises(ValueError):
        calculer_sous_total(-5.0, 2)


def test_refuser_quantite_nulle():
    with pytest.raises(ValueError):
        calculer_sous_total(10.0, 0)


def test_ajouter_article():
    panier = Panier()
    article = Article("Livre Python", "LIVRE", 20.0, 2)

    panier.ajouter(article)

    assert len(panier.articles) == 1
    assert panier.sous_total() == 40.0


def test_modifier_quantite():
    panier = Panier()
    panier.ajouter(Article("Clavier", "STANDARD", 50.0, 1))

    panier.modifier_quantite("Clavier", 3)

    assert panier.sous_total() == 150.0


def test_refuser_quantite_invalide():
    panier = Panier()
    panier.ajouter(Article("Clavier", "STANDARD", 50.0, 1))

    with pytest.raises(ValueError):
        panier.modifier_quantite("Clavier", 0)


def test_retirer_article():
    panier = Panier()
    panier.ajouter(Article("Souris", "STANDARD", 25.0, 2))

    panier.retirer("Souris")

    assert len(panier.articles) == 0
    assert panier.sous_total() == 0.0


def test_refuser_article_introuvable():
    panier = Panier()

    with pytest.raises(ValueError):
        panier.retirer("Article inexistant")


def test_refuser_article_sans_nom():
    with pytest.raises(ValueError):
        Article("", "LIVRE", 10.0, 1)


def test_promo10_reduit_le_total_de_10_pourcent():
    panier = Panier()
    panier.ajouter(Article("Clavier", "STANDARD", 100.0, 1))

    panier.appliquer_promotion("PROMO10")

    assert panier.montant_reduction() == 10.0
    assert panier.total_apres_reduction() == 90.0


def test_code_promo_inconnu_ne_donne_pas_de_reduction():
    panier = Panier()
    panier.ajouter(Article("Clavier", "STANDARD", 100.0, 1))

    panier.appliquer_promotion("INCONNU")

    assert panier.montant_reduction() == 0.0
    assert panier.total_apres_reduction() == 100.0


def test_total_apres_reduction_ne_peut_pas_etre_negatif():
    panier = Panier()
    panier.appliquer_promotion("PROMO10")

    assert panier.total_apres_reduction() == 0.0

def test_tva_livre():
    panier = Panier()
    panier.ajouter(Article("Livre Python", "LIVRE", 100.00))

    assert panier.montant_tva() == 5.50
    assert panier.total_ttc() == 105.50


def test_tva_produit_standard():
    panier = Panier()
    panier.ajouter(Article("Clavier", "STANDARD", 100.00))

    assert panier.montant_tva() == 20.00
    assert panier.total_ttc() == 120.00


def test_tva_apres_promotion():
    panier = Panier()
    panier.ajouter(Article("Clavier", "STANDARD", 100.00))
    panier.appliquer_promotion("PROMO10")

    assert panier.montant_tva() == 18.00
    assert panier.total_ttc() == 108.00



def test_offre_3_pour_4_unites_eligibles():
    panier = Panier()
    panier.ajouter(
        Article("Produit A", "STANDARD", 10.00, 4, True)
    )

    assert panier.montant_reduction_offre() == 10.00


def test_offre_plusieurs_groupes():
    panier = Panier()
    panier.ajouter(
        Article("Produit A", "STANDARD", 10.00, 8, True)
    )

    assert panier.montant_reduction_offre() == 20.00


def test_offre_non_applicable_a_un_produit_non_eligible():
    panier = Panier()
    panier.ajouter(
        Article("Produit A", "STANDARD", 10.00, 4)
    )

    assert panier.montant_reduction_offre() == 0.00


def test_offre_prix_unitaire_le_plus_bas():
    panier = Panier()
    panier.ajouter(
        Article("Produit A", "STANDARD", 5.00, 1, True)
    )
    panier.ajouter(
        Article("Produit B", "STANDARD", 8.00, 1, True)
    )
    panier.ajouter(
        Article("Produit C", "STANDARD", 12.00, 1, True)
    )
    panier.ajouter(
        Article("Produit D", "STANDARD", 20.00, 1, True)
    )

    assert panier.montant_reduction_offre() == 5.00


def test_offre_moins_de_quatre_unites():
    panier = Panier()
    panier.ajouter(
        Article("Produit A", "STANDARD", 10.00, 3, True)
    )

    assert panier.montant_reduction_offre() == 0.00

def test_offre_appliquee_avant_promo10():
    panier = Panier()
    panier.ajouter(Article("A", "STANDARD", 10, 4, True))
    panier.appliquer_promotion("PROMO10")

    assert panier.montant_reduction_offre() == 10.00
    assert panier.montant_reduction() == 3.00
    assert panier.total_apres_reduction() == 27.00


def test_promo10_appliquee_apres_offre():
    panier = Panier()
    panier.ajouter(Article("A", "STANDARD", 10, 4, True))
    panier.ajouter(Article("B", "STANDARD", 20, 1, False))
    panier.appliquer_promotion("PROMO10")

    assert panier.montant_reduction_offre() == 10.00
    assert panier.montant_reduction() == 5.00
    assert panier.total_apres_reduction() == 45.00


def test_reductions_ne_peuvent_pas_rendre_total_negatif():
    panier = Panier()
    panier.ajouter(Article("A", "STANDARD", 10, 4, True))

    assert panier.total_apres_reduction() >= 0.00


def test_total_ttc_coherent_avec_ht_et_tva_apres_offre():
    panier = Panier()
    panier.ajouter(Article("A", "STANDARD", 10, 4, True))
    panier.appliquer_promotion("PROMO10")

    total_ht = panier.total_apres_reduction()
    tva = panier.montant_tva()
    total_ttc = panier.total_ttc()

    assert total_ht == 27.00
    assert tva == 5.40
    assert total_ttc == round(total_ht + tva, 2)



def test_offre_sur_plusieurs_articles_a_prix_differents():
    panier = Panier()
    panier.ajouter(Article("A", "STANDARD", 5, 1, True))
    panier.ajouter(Article("B", "STANDARD", 8, 1, True))
    panier.ajouter(Article("C", "STANDARD", 12, 1, True))
    panier.ajouter(Article("D", "STANDARD", 20, 1, True))

    assert panier.sous_total() == 45.00
    assert panier.montant_reduction_offre() == 5.00


def test_tva_apres_offre_sur_plusieurs_articles():
    panier = Panier()
    panier.ajouter(Article("A", "STANDARD", 5, 1, True))
    panier.ajouter(Article("B", "STANDARD", 8, 1, True))
    panier.ajouter(Article("C", "STANDARD", 12, 1, True))
    panier.ajouter(Article("D", "LIVRE", 20, 1, True))
    panier.appliquer_promotion("PROMO10")

    assert panier.sous_total() == 45.00
    assert panier.montant_reduction_offre() == 5.00
    assert panier.montant_reduction() == 4.00
    assert panier.total_apres_reduction() == 36.00
    assert panier.montant_tva() == 4.59
    assert panier.total_ttc() == 40.59

def test_tva_standard_apres_promotion():
    panier = Panier()
    panier.ajouter(Article("Produit test", "STANDARD", 100, 1))
    panier.appliquer_promotion("PROMO10")

    assert panier.sous_total() == 100.00
    assert panier.total_apres_reduction() == 90.00

    # Échec volontaire pour simuler la détection d'un défaut
    assert panier.montant_tva() == 18.00