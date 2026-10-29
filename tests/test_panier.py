
from panierplus.panier import calculer_sous_total


def test_module_panier_est_importable():
    assert callable(calculer_sous_total)
