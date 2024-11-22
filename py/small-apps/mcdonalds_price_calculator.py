import numpy as np
from scipy.optimize import minimize

class ProductPricing:
    def __init__(self):
        self.products = []
        self.equations = []
        self.loyalty_point_rates = {}

    def add_product(self, product_name):
        if product_name not in self.products:
            self.products.append(product_name)

    def add_equation(self, product_counts, price, tolerance=2.0):
        """
        Dodaj zestaw.
        :param product_counts: dict, liczba sztuk każdego produktu w zestawie (np. {"Item A": 1, "Item B": 2}).
        :param price: float, cena zestawu.
        :param tolerance: float, dopuszczalna odchyłka od ceny zestawu.
        """
        self.equations.append({"counts": product_counts, "price": price, "tolerance": tolerance})

    def set_loyalty_rate(self, product_name, points):
        """
        Ustaw liczbę punktów lojalnościowych dla produktu.
        :param product_name: str, nazwa produktu.
        :param points: float, liczba punktów lojalnościowych.
        """
        self.loyalty_point_rates[product_name] = points

    def solve(self):
        # przypisz indeksy produktom
        product_index = {product: i for i, product in enumerate(self.products)}
        n = len(self.products)

        # funkcja celu do minimalizacji
        def loss_function(prices):
            error = 0
            for eq in self.equations:
                predicted_price = sum(prices[product_index[prod]] * count
                                      for prod, count in eq["counts"].items())
                diff = predicted_price - eq["price"]
                error += (diff / eq["tolerance"])**2  # uwzględnij tolerancję
            return error

        # początkowe zgadywanie cen (np. wszystkie po 1 zł)
        initial_guess = np.ones(n)

        # ograniczenia (ceny muszą być >= 0)
        bounds = [(0, None)] * n

        # rozwiązanie
        result = minimize(loss_function, initial_guess, bounds=bounds)
        prices = result.x

        # oblicz niepewności
        uncertainties = []
        for i in range(n):
            perturbed_prices = prices.copy()
            perturbed_prices[i] += 0.1  # małe zaburzenie
            perturbed_error = loss_function(perturbed_prices)
            uncertainties.append(np.sqrt(abs(perturbed_error - loss_function(prices))))

        self.prices = {product: (price, uncertainty) for product, price, uncertainty
                       in zip(self.products, prices, uncertainties)}

    def get_product_prices(self):
        return self.prices

    def get_equation_costs(self):
        """
        Oblicz koszty zestawów na podstawie obecnych szacunków cen produktów.
        :return: lista słowników z rzeczywistą ceną, przewidywaną ceną i różnicą.
        """
        results = []
        for eq in self.equations:
            predicted_price = sum(self.prices[prod][0] * count
                                  for prod, count in eq["counts"].items())
            results.append({
                "actual_price": eq["price"],
                "predicted_price": predicted_price,
                "difference": abs(predicted_price - eq["price"])
            })
        return results


if __name__ == "__main__":
    # utwórz obiekt
    pricing = ProductPricing()

    # dodaj produkty
    pricing.add_product("Item A")
    pricing.add_product("Item B")
    pricing.add_product("Item C")

    # dodaj równania (zestawy)
    pricing.add_equation({"Item A": 1, "Item B": 2}, 18, tolerance=2)
    pricing.add_equation({"Item A": 2, "Item C": 1}, 25, tolerance=1.5)
    pricing.add_equation({"Item B": 3, "Item C": 1}, 30, tolerance=3)

    # ustaw punkty lojalnościowe
    pricing.set_loyalty_rate("Item A", 10)
    pricing.set_loyalty_rate("Item C", 15)

    # oblicz ceny
    pricing.solve()

    # pokaż ceny produktów
    print("Product prices with uncertainties:")
    for product, (price, uncertainty) in pricing.get_product_prices().items():
        print(f"{product}: {price:.2f} ± {uncertainty:.2f} zł")

    # pokaż koszty zestawów
    print("\nEquation costs:")
    for eq_cost in pricing.get_equation_costs():
        print(eq_cost)
