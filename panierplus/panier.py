"""Core module for the PanierPlus shopping cart."""




def calculer_sous_total(prix_unitaire: float, quantite: int) -> float:
    """Calculate the subtotal for one product."""
    if prix_unitaire < 0:
        raise ValueError("Le prix unitaire doit être positif ou nul.")
    if quantite <= 0:
        raise ValueError("La quantité doit être strictement positive.")
    return prix_unitaire * quantite
