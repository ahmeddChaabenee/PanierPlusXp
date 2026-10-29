from decimal import Decimal

import pytest

from panierplus.panier import (
    calculer_promo10,
    calculer_promo_trois_achetes_un_gratuit,
    calculer_sous_total,
    calculer_ttc,
    plafonner_reduction,
)


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


def test_promo10_refuse_un_montant_negatif():
    with pytest.raises(ValueError):
        calculer_promo10(Decimal("-10.00"))


def test_promo10_arrondit_a_deux_decimales():
    montant = Decimal("10.05")

    assert calculer_promo10(montant) == Decimal("1.01")


def test_promo10_accepte_un_montant_nul():
    assert calculer_promo10(Decimal("0.00")) == Decimal("0.00")


def test_promo10_sur_un_montant_inferieur_a_dix():
    assert calculer_promo10(Decimal("5.00")) == Decimal("0.50")

def test_promo10_ne_depasse_pas_le_montant_eligible():
    montant = Decimal("5.00")
    reduction = calculer_promo10(montant)

    assert reduction <= montant

def test_calculer_ttc_avec_tva_19_pourcent():
    montant_ht = Decimal("100.00")

    assert calculer_ttc(montant_ht) == Decimal("119.00")

def test_calculer_ttc_refuse_un_montant_negatif():
    with pytest.raises(ValueError):
        calculer_ttc(Decimal("-10.00"))



def test_calculer_ttc_accepte_un_montant_nul():
    assert calculer_ttc(Decimal("0.00")) == Decimal("0.00")


def test_calculer_ttc_arrondit_a_deux_decimales():
    montant_ht = Decimal("10.05")

    assert calculer_ttc(montant_ht) == Decimal("11.96")


def test_promo_trois_achetes_un_gratuit():
    prix_unitaire = Decimal("10.00")
    quantite = 4

    assert calculer_promo_trois_achetes_un_gratuit(
        prix_unitaire, quantite
    ) == Decimal("10.00")


def test_promo_trois_achetes_un_gratuit_sans_quatrieme_article():
    prix_unitaire = Decimal("10.00")
    quantite = 3

    assert calculer_promo_trois_achetes_un_gratuit(
        prix_unitaire, quantite
    ) == Decimal("0.00")


def test_promo_trois_achetes_un_gratuit_pour_huit_articles():
    prix_unitaire = Decimal("10.00")
    quantite = 8

    assert calculer_promo_trois_achetes_un_gratuit(
        prix_unitaire, quantite
    ) == Decimal("20.00")


def test_promo_trois_achetes_un_gratuit_refuse_prix_negatif():
    with pytest.raises(ValueError):
        calculer_promo_trois_achetes_un_gratuit(
            Decimal("-10.00"), 4
        )



def test_promo_trois_achetes_un_gratuit_refuse_quantite_negative():
    with pytest.raises(ValueError):
        calculer_promo_trois_achetes_un_gratuit(
            Decimal("10.00"), -1
        )


def test_reduction_totale_ne_depasse_pas_le_montant_eligible():
    montant_eligible = Decimal("5.00")
    reduction_promo10 = calculer_promo10(montant_eligible)
    reduction_3_achetes_1_gratuit = Decimal("10.00")

    reduction_totale = min(
        reduction_promo10 + reduction_3_achetes_1_gratuit,
        montant_eligible,
    )

    assert reduction_totale == Decimal("5.00")


def test_plafonner_reduction_au_montant_eligible():
    montant_eligible = Decimal("5.00")
    reduction = Decimal("10.00")

    assert plafonner_reduction(
        reduction, montant_eligible
    ) == Decimal("5.00")


def test_plafonner_reduction_refuse_une_reduction_negative():
    with pytest.raises(ValueError):
        plafonner_reduction(
            Decimal("-1.00"),
            Decimal("10.00"),
        )


def test_plafonner_reduction_refuse_un_montant_eligible_negatif():
    with pytest.raises(ValueError):
        plafonner_reduction(
            Decimal("1.00"),
            Decimal("-10.00"),
        )


def test_plafonner_reduction_accepte_zero():
    assert plafonner_reduction(
        Decimal("0.00"),
        Decimal("10.00"),
    ) == Decimal("0.00")


def test_plafonner_reduction_ne_depasse_pas_le_montant_eligible():
    assert plafonner_reduction(
        Decimal("3.00"),
        Decimal("5.00"),
    ) == Decimal("3.00")


def test_plafonner_reduction_egale_au_montant_eligible():
    assert plafonner_reduction(
        Decimal("5.00"),
        Decimal("5.00"),
    ) == Decimal("5.00")