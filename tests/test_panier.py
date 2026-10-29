
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
