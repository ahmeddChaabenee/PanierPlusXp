
"""Core logic for the PanierPlus shopping cart."""

from dataclasses import dataclass


@dataclass
class Article:
    nom: str
    categorie: str
    prix_unitaire: float
    quantite: int = 1

    def __post_init__(self):
        if not self.nom.strip():
            raise ValueError("Le nom de l'article est obligatoire.")
        if self.prix_unitaire < 0:
            raise ValueError("Le prix ne peut pas être négatif.")
        if self.quantite <= 0:
            raise ValueError("La quantité doit être positive.")


class Panier:
    def __init__(self):
        self.articles = []

    def ajouter(self, article: Article) -> None:
        self.articles.append(article)

    def modifier_quantite(self, nom: str, quantite: int) -> None:
        if quantite <= 0:
            raise ValueError("La quantité doit être positive.")

        for article in self.articles:
            if article.nom == nom:
                article.quantite = quantite
                return

        raise ValueError(f"Article introuvable : {nom}")

    def retirer(self, nom: str) -> None:
        for article in self.articles:
            if article.nom == nom:
                self.articles.remove(article)
                return

        raise ValueError(f"Article introuvable : {nom}")

    def sous_total(self) -> float:
        return round(
            sum(
                article.prix_unitaire * article.quantite
                for article in self.articles
            ),
            2,
        )


def calculer_sous_total(prix_unitaire: float, quantite: int) -> float:
    """Return the subtotal for one product."""
    if prix_unitaire < 0:
        raise ValueError("Le prix ne peut pas être négatif.")
    if quantite <= 0:
        raise ValueError("La quantité doit être positive.")

    return round(prix_unitaire * quantite, 2)
