"""Core module for the PanierPlus shopping cart."""


def calculer_sous_total(prix_unitaire: float, quantite: int) -> float:
    """Calculate the subtotal for one product."""
    return prix_unitaire * quantite
