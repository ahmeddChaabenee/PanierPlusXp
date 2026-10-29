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



def calculer_promo_trois_achetes_un_gratuit(
    prix_unitaire: Decimal,
    quantite: int,
) -> Decimal:
    """Calcule la réduction pour chaque groupe de 4 articles : 1 gratuit."""
    if prix_unitaire < Decimal("0.00"):
        raise ValueError("Le prix unitaire doit être positif ou nul.")
    if quantite < 0:
        raise ValueError("La quantité doit être positive ou nulle.")

    articles_gratuits = quantite // 4
    reduction = prix_unitaire * articles_gratuits

    return reduction.quantize(
        Decimal("0.01"),
        rounding=ROUND_HALF_UP,
    )



def plafonner_reduction(
    reduction: Decimal,
    montant_eligible: Decimal,
) -> Decimal:
    """Limite la réduction au montant éligible."""
    if reduction < Decimal("0.00"):
        raise ValueError("La réduction doit être positive ou nulle.")
    if montant_eligible < Decimal("0.00"):
        raise ValueError("Le montant éligible doit être positif ou nul.")

    reduction_plafonnee = min(reduction, montant_eligible)

    return reduction_plafonnee.quantize(
        Decimal("0.01"),
        rounding=ROUND_HALF_UP,
    )

def calculer_promo10(
    montant: Decimal,
    categorie: str | None = None,
) -> Decimal:
    """Calcule une réduction de 10 %, sauf pour les livres."""
    if montant < Decimal("0.00"):
        raise ValueError("Le montant doit être positif ou nul.")

    if categorie is not None and categorie.strip().lower() == "livre":
        return Decimal("0.00")

    return (montant * Decimal("0.10")).quantize(
        Decimal("0.01"),
        rounding=ROUND_HALF_UP,
    )