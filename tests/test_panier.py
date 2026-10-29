from decimal import Decimal

import pytest

from panierplus.panier import calculer_sous_total

from panierplus.panier import calculer_sous_total, calculer_promo10


def test_module_panier_est_importable():
    assert callable(calculer_sous_total)


def test_calculer_sous_total():
    assert calculer_sous_total(10.0, 3) == 30.0

def test_calculer_sous_total_avec_decimal():
    assert calculer_sous_total(Decimal("10.00"), 3) == Decimal("30.00")
def test_quantite_nulle_est_refusee():
    with pytest.raises(ValueError):
        calculer_sous_total(Decimal("10.00"), 0)
def test_quantite_negative_est_refusee():
    with pytest.raises(ValueError):
        calculer_sous_total(Decimal("10.00"), -1)
def test_prix_negatif_est_refuse():
    with pytest.raises(ValueError):
        calculer_sous_total(Decimal("-10.00"), 2)
def test_prix_nul_est_accepte():
    assert calculer_sous_total(Decimal("0.00"), 2) == Decimal("0.00")


def test_promo10_applique_une_reduction_de_10_pourcent():
    montant = Decimal("100.00")

    assert calculer_promo10(montant) == Decimal("10.00")

