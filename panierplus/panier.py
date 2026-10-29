
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

    def _unites_gratuites_par_article(self) -> dict[int, int]:
        """Return the number of free offer units for each article."""
        unites_eligibles = []

        for article in self.articles:
            if article.eligible_offre:
                prix = montant(article.prix_unitaire)
                unites_eligibles.extend(
                    (prix, article) for _ in range(article.quantite)
                )

        # Sort from most expensive to least expensive.
        unites_eligibles.sort(key=lambda element: element[0], reverse=True)

        gratuites_par_article = {}

        # One free unit for every group of four eligible units.
        for index in range(3, len(unites_eligibles), 4):
            _, article = unites_eligibles[index]
            article_id = id(article)
            gratuites_par_article[article_id] = (
                gratuites_par_article.get(article_id, 0) + 1
            )

        return gratuites_par_article

    def montant_reduction_offre(self) -> float:
        """Calculate the 3-for-1 discount on eligible products."""
        gratuites = self._unites_gratuites_par_article()

        reduction = sum(
            (
                montant(article.prix_unitaire)
                * gratuites.get(id(article), 0)
                for article in self.articles
            ),
            ZERO,
        )

        return float(montant(reduction))

    def montant_reduction(self) -> float:
        """Calculate PROMO10 after the offer, excluding books."""
        if self.code_promo != "PROMO10":
            return 0.0

        gratuites = self._unites_gratuites_par_article()
        base_promo = ZERO

        for article in self.articles:
            if article.categorie.upper() != "STANDARD":
                continue

            quantite_gratuite = gratuites.get(id(article), 0)
            quantite_payante = max(
                article.quantite - quantite_gratuite,
                0,
            )

            base_promo += (
                montant(article.prix_unitaire) * quantite_payante
            )

        reduction = montant(base_promo * TAUX_PROMO)
        return float(min(reduction, base_promo))

    def total_apres_reduction(self) -> float:
        """Return the non-negative total HT after all discounts."""
        sous_total = montant(self.sous_total())
        reduction_offre = min(
            montant(self.montant_reduction_offre()),
            sous_total,
        )

        montant_restant = max(sous_total - reduction_offre, ZERO)
        reduction_promo = montant(self.montant_reduction())

        reduction_promo = min(reduction_promo, montant_restant)
        total = montant_restant - reduction_promo

        return float(max(total, ZERO))

    def montant_tva(self) -> float:
        """Calculate VAT after the applicable discounts."""
        taux_tva = {
            "LIVRE": Decimal("0.055"),
            "STANDARD": Decimal("0.20"),
        }

        gratuites = self._unites_gratuites_par_article()
        total_tva = ZERO

        for article in self.articles:
            categorie = article.categorie.upper()
            taux = taux_tva.get(categorie)

            if taux is None:
                raise ValueError(f"Catégorie inconnue : {article.categorie}")

            quantite_gratuite = gratuites.get(id(article), 0)
            quantite_payante = max(
                article.quantite - quantite_gratuite,
                0,
            )

            montant_ligne = montant(
                montant(article.prix_unitaire) * quantite_payante
            )

            # PROMO10 applies only to STANDARD products.
            if self.code_promo == "PROMO10" and categorie == "STANDARD":
                reduction_ligne = montant(montant_ligne * TAUX_PROMO)
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
