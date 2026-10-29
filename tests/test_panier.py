from panierplus.panier import calculer_sous_total


def test_module_panier_est_importable():
    assert callable(calculer_sous_total)


def test_calculer_sous_total():
    assert calculer_sous_total(10.0, 3) == 30.0