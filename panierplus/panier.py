
"""Core logic for the PanierPlus shopping cart."""

from dataclasses import dataclass
from decimal import ROUND_HALF_UP, Decimal


def montant(valeur: float | str | Decimal) -> Decimal:
    """Convert a value to a monetary amount with two decimal places."""
    return Decimal(str(valeur)).quantize(
        Decimal("0.01"),
        rounding=ROUND_HALF_UP,
    )


@dataclass
class Article:
    nom: str
    categorie: str
    prix_unitaire: float
    quantite: int = 1
    eligible_offre: bool = False

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
        self.code_promo = None

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
        total = sum(
            (
                montant(article.prix_unitaire) * article.quantite
                for article in self.articles
            ),
            Decimal("0.00"),
        )
        return float(montant(total))

    def appliquer_promotion(self, code: str) -> None:
        """Apply a recognized promotion code."""
        self.code_promo = code if code == "PROMO10" else None

    def montant_reduction(self) -> float:
        """Calculate the PROMO10 discount."""
        if self.code_promo != "PROMO10":
            return 0.0

        reduction = montant(
            Decimal(str(self.sous_total())) * Decimal("0.10")
        )
        reduction = min(reduction, montant(self.sous_total()))
        return float(reduction)

    def total_apres_reduction(self) -> float:
        """Return the total after the PROMO10 discount."""
        total = montant(self.sous_total()) - montant(
            self.montant_reduction()
        )
        return float(max(total, Decimal("0.00")))

    def montant_tva(self) -> float:
        """Calculate VAT on each product after promotion."""
        taux_tva = {
            "LIVRE": Decimal("0.055"),
            "STANDARD": Decimal("0.20"),
        }

        total_tva = Decimal("0.00")

        for article in self.articles:
            taux = taux_tva.get(article.categorie.upper())

            if taux is None:
                raise ValueError(
                    f"Catégorie inconnue : {article.categorie}"
                )

            montant_ligne = (
                montant(article.prix_unitaire) * article.quantite
            )

            if self.code_promo == "PROMO10":
                reduction_ligne = montant(
                    montant_ligne * Decimal("0.10")
                )
                montant_ligne = max(
                    montant_ligne - reduction_ligne,
                    Decimal("0.00"),
                )

            total_tva += montant(montant_ligne * taux)

        return float(montant(total_tva))

    def total_ttc(self) -> float:
        """Return the total including VAT after promotion."""
        total_ht = montant(self.total_apres_reduction())
        tva = montant(self.montant_tva())
        return float(montant(total_ht + tva))

    def montant_reduction_offre(self) -> float:
        """Calculate the 3-for-1 discount for eligible products."""
        prix_unites = []

        for article in self.articles:
            if article.eligible_offre:
                prix = montant(article.prix_unitaire)
                prix_unites.extend([prix] * article.quantite)

        # Group units from most expensive to least expensive.
        prix_unites.sort(reverse=True)

        reduction = Decimal("0.00")

        for index in range(3, len(prix_unites), 4):
            reduction += prix_unites[index]

        return float(montant(reduction))


def calculer_sous_total(
    prix_unitaire: float,
    quantite: int,
) -> float:
    """Return the subtotal for one product."""
    if prix_unitaire < 0:
        raise ValueError("Le prix ne peut pas être négatif.")
    if quantite <= 0:
        raise ValueError("La quantité doit être positive.")

    return float(montant(montant(prix_unitaire) * quantite))
