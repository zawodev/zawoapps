import json
import numpy as np

def load_data(filename):
    """loads data from a JSON file"""
    with open(filename, 'r') as file:
        return json.load(file)

def calculate_product_prices(data, main_currency):
    """calculates approximate product prices in the main currency"""
    products = set()
    equations = []
    values = []
    conversion_equations = []

    for item in data["sets"]:
        unified_price = 0
        main_price_found = False
        for price_entry in item["price"]:
            if price_entry["currency"] == main_currency:
                unified_price += price_entry["value"]
                main_price_found = True
            else:
                # keep track of other currencies for later
                conversion_equations.append((item["products"], price_entry["value"], price_entry["currency"]))

        if main_price_found:
            equation = {}
            for product, quantity in item["products"].items():
                equation[product] = equation.get(product, 0) + quantity
                products.add(product)
            equations.append(equation)
            values.append(unified_price)

    products = sorted(products)
    coefficients = []
    for equation in equations:
        row = [equation.get(product, 0) for product in products]
        coefficients.append(row)

    # solve for product prices in the main currency
    coefficients = np.array(coefficients)
    values = np.array(values)
    product_prices, _, _, _ = np.linalg.lstsq(coefficients, values, rcond=None)

    product_prices_dict = dict(zip(products, product_prices))

    # calculate conversion rates to secondary currencies
    conversion_rates = {}
    for products, other_price, other_currency in conversion_equations:
        estimated_price = sum(product_prices_dict[product] * quantity for product, quantity in products.items())
        if estimated_price > 0:  # avoid division by zero
            rate = other_price / estimated_price
            if other_currency not in conversion_rates:
                conversion_rates[other_currency] = []
            conversion_rates[other_currency].append(rate)

    # average conversion rates
    averaged_rates = {cur: sum(rates) / len(rates) for cur, rates in conversion_rates.items()}

    return product_prices_dict, averaged_rates

def calculate_set_quality(data, product_prices, main_currency):
    qualities = []
    for item in data["sets"]:
        actual_prices = [
            price_entry["value"] for price_entry in item["price"] if price_entry["currency"] == main_currency
        ]
        if not actual_prices:
            # if the set has no price in the main currency, append a default value
            qualities.append(0.0)
            continue
        actual_price = sum(actual_prices)
        estimated_price = sum(product_prices[product] * quantity
                              for product, quantity in item["products"].items())
        quality = estimated_price / actual_price
        qualities.append(min(1.0, max(0.0, quality)))  # ensure 0.0 <= quality <= 1.0
    return qualities


def convert_prices(product_prices, rates, target_currency, main_currency):
    """converts product prices to a target currency"""
    if target_currency == main_currency:
        return product_prices
    if target_currency in rates:
        rate = rates[target_currency]
        return {product: price * rate for product, price in product_prices.items()}
    else:
        return {}

def main(filename, main_currency, target_currency):
    data = load_data(filename)
    product_prices, conversion_rates = calculate_product_prices(data, main_currency)
    qualities = calculate_set_quality(data, product_prices, main_currency)
    converted_prices = convert_prices(product_prices, conversion_rates, target_currency, main_currency)

    print(f"Approximate Product Prices in {main_currency}:")
    for product, price in product_prices.items():
        print(f"{product}: {price:.2f} {main_currency}")

    if target_currency != main_currency:
        print(f"\nApproximate Product Prices in {target_currency}:")
        for product, price in converted_prices.items():
            print(f"{product}: {price:.2f} {target_currency}")

    print("\nSet Qualities:")
    for i, item in enumerate(data["sets"]):
        name = item["name"]
        quality = qualities[i] if i < len(qualities) else 0.0  # ensure no out-of-range access
        print(f"{name}: Quality: {quality:.2f}")


if __name__ == "__main__":
    # Example usage
    main('mcdonalds.json', 'PKT', 'PLN')
