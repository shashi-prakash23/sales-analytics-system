import requests

BASE_URL = "https://dummyjson.com/products"


def fetch_all_products():
    """
    Fetches all products from DummyJSON API

    Returns: list of product dictionaries
    """

    try:
        response = requests.get(f"{BASE_URL}?limit=100", timeout=10)
        response.raise_for_status()

        data = response.json()
        products = data.get("products", [])

        print(f"Successfully fetched {len(products)} products from API")
        return products

    except requests.exceptions.RequestException as e:
        print("Failed to fetch products from API:", e)
        return []

def create_product_mapping(api_products):
    """
    Creates a mapping of product IDs to product info

    Returns: dictionary mapping product IDs to info
    """

    product_mapping = {}

    for product in api_products:
        product_id = product.get("id")

        if product_id is None:
            continue

        product_mapping[product_id] = {
            "title": product.get("title"),
            "category": product.get("category"),
            "brand": product.get("brand"),
            "rating": product.get("rating")
        }

    return product_mapping


import re


def enrich_sales_data(transactions, product_mapping):
    """
    Enriches transaction data with API product information

    Returns: list of enriched transaction dictionaries
    """

    enriched_transactions = []

    for txn in transactions:
        enriched_txn = txn.copy()

        try:
            # Extract numeric product ID (P101 → 101, P5 → 5)
            match = re.search(r"\d+", txn["ProductID"])
            api_product_id = int(match.group()) if match else None

            if api_product_id in product_mapping:
                api_data = product_mapping[api_product_id]

                enriched_txn["API_Category"] = api_data.get("category")
                enriched_txn["API_Brand"] = api_data.get("brand")
                enriched_txn["API_Rating"] = api_data.get("rating")
                enriched_txn["API_Match"] = True
            else:
                enriched_txn["API_Category"] = None
                enriched_txn["API_Brand"] = None
                enriched_txn["API_Rating"] = None
                enriched_txn["API_Match"] = False

        except Exception:
            enriched_txn["API_Category"] = None
            enriched_txn["API_Brand"] = None
            enriched_txn["API_Rating"] = None
            enriched_txn["API_Match"] = False

        enriched_transactions.append(enriched_txn)

    return enriched_transactions

def save_enriched_data(enriched_transactions, filename="data/enriched_sales_data.txt"):
    """
    Saves enriched transactions back to file
    """

    headers = [
        "TransactionID", "Date", "ProductID", "ProductName",
        "Quantity", "UnitPrice", "CustomerID", "Region",
        "API_Category", "API_Brand", "API_Rating", "API_Match"
    ]

    try:
        with open(filename, "w", encoding="utf-8") as file:
            file.write("|".join(headers) + "\n")

            for txn in enriched_transactions:
                row = [
                    str(txn.get("TransactionID", "")),
                    str(txn.get("Date", "")),
                    str(txn.get("ProductID", "")),
                    str(txn.get("ProductName", "")),
                    str(txn.get("Quantity", "")),
                    str(txn.get("UnitPrice", "")),
                    str(txn.get("CustomerID", "")),
                    str(txn.get("Region", "")),
                    str(txn.get("API_Category") or ""),
                    str(txn.get("API_Brand") or ""),
                    str(txn.get("API_Rating") or ""),
                    str(txn.get("API_Match"))
                ]

                file.write("|".join(row) + "\n")

        print(f"Enriched data saved to {filename}")

    except Exception as e:
        print("Failed to save enriched data:", e)
