
"""Core logic for the PanierPlus shopping cart."""

from dataclasses import dataclass
from decimal import ROUND_HALF_UP, Decimal

CENTIME = Decimal("0.01")
ZERO = Decimal("0.00")
TAUX_PROMO = Decimal("0.10")


def montant(valeur: float | str | Decimal) -> Decimal:
    """Convert a value to a monetary amount with two decimal places."""
    return Decimal(str(valeur)).quantize(
        CENTIME,
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
        if montant(self.prix_unitaire) < ZERO:
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
            ZERO,
        )
        return float(montant(total))

    def appliquer_promotion(self, code: str) -> None:
        """Apply a recognized promotion code."""
        self.code_promo = code if code == "PROMO10" else None

    def montant_reduction_offre(self) -> float:
        """Calculate the 3-for-1 discount on eligible products."""
        prix_unites = []

        for article in self.articles:
            if article.eligible_offre:
                prix = montant(article.prix_unitaire)
                prix_unites.extend([prix] * article.quantite)

        # Group eligible units from most expensive to least expensive.
        prix_unites.sort(reverse=True)

        reduction = ZERO

        # One free unit for every group of four eligible units.
        # The cheapest unit in each group is free.
        for index in range(3, len(prix_unites), 4):
            reduction += prix_unites[index]

        return float(montant(reduction))

    def montant_reduction(self) -> float:
        """Calculate PROMO10 after the 3-for-1 offer."""
        if self.code_promo != "PROMO10":
            return 0.0

        sous_total = montant(self.sous_total())
        reduction_offre = montant(self.montant_reduction_offre())

        montant_restant = max(
            sous_total - reduction_offre,
            ZERO,
        )

        reduction = montant(montant_restant * TAUX_PROMO)

        return float(min(reduction, montant_restant))

    def total_apres_reduction(self) -> float:
        """Return the non-negative total HT after all discounts."""
        sous_total = montant(self.sous_total())
        reduction_offre = montant(self.montant_reduction_offre())

        reduction_offre = min(reduction_offre, sous_total)
        montant_restant = max(sous_total - reduction_offre, ZERO)

        if self.code_promo == "PROMO10":
            reduction_promo = montant(
                montant_restant * TAUX_PROMO
            )
            reduction_promo = min(reduction_promo, montant_restant)
        else:
            reduction_promo = ZERO

        total = montant_restant - reduction_promo
        return float(max(total, ZERO))

    def montant_tva(self) -> float:
        """Calculate VAT on each product after applicable discounts."""
        taux_tva = {
            "LIVRE": Decimal("0.055"),
            "STANDARD": Decimal("0.20"),
        }

        # Calculate the offer discount per eligible product line.
        unites_eligibles = []
        for article in self.articles:
            if article.eligible_offre:
                for _ in range(article.quantite):
                    unites_eligibles.append(
                        (montant(article.prix_unitaire), article)
                    )

        # The lowest-priced unit in every group of four is free.
        unites_eligibles.sort(
            key=lambda element: element[0],
            reverse=True,
        )

        unites_gratuites = set()
        for index in range(3, len(unites_eligibles), 4):
            unites_gratuites.add(index)

        # Track free units by article identity and unit position.
        gratuites_par_article = {}
        for index in unites_gratuites:
            prix, article = unites_eligibles[index]
            gratuites_par_article.setdefault(id(article), []).append(prix)

        # Allocate the offer discount across lines proportionally to
        # the actual free units selected by the offer.
        reductions_offre_par_article = {}
        for prix, article in unites_eligibles:
            reductions_offre_par_article.setdefault(id(article), [])

        # Reconstruct the free-unit count for each article.
        gratuites_par_article = {}
        for index in range(3, len(unites_eligibles), 4):
            _, article = unites_eligibles[index]
            gratuites_par_article[id(article)] = (
                gratuites_par_article.get(id(article), 0) + 1
            )

        total_tva = ZERO

        for article in self.articles:
            taux = taux_tva.get(article.categorie.upper())
            if taux is None:
                raise ValueError(
                    f"Catégorie inconnue : {article.categorie}"
                )

            montant_ligne = (
                montant(article.prix_unitaire) * article.quantite
            )

            reduction_offre_ligne = (
                montant(article.prix_unitaire)
                * gratuites_par_article.get(id(article), 0)
            )

            montant_ligne = max(
                montant_ligne - reduction_offre_ligne,
                ZERO,
            )

            # PROMO10 is applied after the offer to the remaining
            # amount of the product line.
            if self.code_promo == "PROMO10":
                reduction_ligne = montant(
                    montant_ligne * TAUX_PROMO
                )
                montant_ligne = max(
                    montant_ligne - reduction_ligne,
                    ZERO,
                )

            total_tva += montant(montant_ligne * taux)

        return float(montant(total_tva))

    def total_ttc(self) -> float:
        """Return the total including VAT after all discounts."""
        total_ht = montant(self.total_apres_reduction())
        tva = montant(self.montant_tva())
        return float(montant(total_ht + tva))


def calculer_sous_total(
    prix_unitaire: float,
    quantite: int,
) -> float:
    """Return the subtotal for one product."""
    if montant(prix_unitaire) < ZERO:
        raise ValueError("Le prix ne peut pas être négatif.")
    if quantite <= 0:
        raise ValueError("La quantité doit être positive.")

    return float(montant(montant(prix_unitaire) * quantite))
