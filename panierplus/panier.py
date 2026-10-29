"""Core module for the PanierPlus shopping cart."""

from decimal import ROUND_HALF_UP, Decimal


def calculer_sous_total(prix_unitaire: float, quantite: int) -> float:
    """Calculate the subtotal for one product."""
    if prix_unitaire < 0:
        raise ValueError("Le prix unitaire doit être positif ou nul.")
    if quantite <= 0:
        raise ValueError("La quantité doit être strictement positive.")
    return prix_unitaire * quantite


def calculer_promo10(montant: Decimal) -> Decimal:
    """Calcule une réduction de 10 % sur un montant."""
    if montant < Decimal("0.00"):
        raise ValueError("Le montant doit être positif ou nul.")
    return (montant * Decimal("0.10")).quantize(
        Decimal("0.01"),
        rounding=ROUND_HALF_UP,
    )


def calculer_ttc(montant_ht: Decimal) -> Decimal:
    """Calcule le montant TTC avec une TVA de 19 %."""
    if montant_ht < Decimal("0.00"):
        raise ValueError("Le montant HT doit être positif ou nul.")

    taux_tva = Decimal("0.19")
    montant_ttc = montant_ht * (Decimal("1.00") + taux_tva)

    return montant_ttc.quantize(
        Decimal("0.01"),
        rounding=ROUND_HALF_UP,
    )