def parse_transactions(raw_lines):
    """
    Parses raw lines into clean list of dictionaries

    Returns: list of dictionaries with keys:
    ['TransactionID', 'Date', 'ProductID', 'ProductName',
     'Quantity', 'UnitPrice', 'CustomerID', 'Region']
    """

    transactions = []

    for line in raw_lines:
        parts = line.split("|")

        # Skip rows with incorrect number of fields
        if len(parts) != 8:
            continue

        try:
            transaction_id = parts[0].strip()
            date = parts[1].strip()
            product_id = parts[2].strip()

            # Remove commas from ProductName
            product_name = parts[3].replace(",", "").strip()

            # Remove commas from numeric fields
            quantity = int(parts[4].replace(",", "").strip())
            unit_price = float(parts[5].replace(",", "").strip())

            customer_id = parts[6].strip()
            region = parts[7].strip()

            transactions.append({
                "TransactionID": transaction_id,
                "Date": date,
                "ProductID": product_id,
                "ProductName": product_name,
                "Quantity": quantity,
                "UnitPrice": unit_price,
                "CustomerID": customer_id,
                "Region": region
            })

        except ValueError:
            # Skip rows with conversion issues
            continue

    return transactions

def calculate_total_revenue(transactions):
    """
    Calculates total revenue from all transactions

    Returns: float (total revenue)
    """

    total_revenue = 0.0

    for txn in transactions:
        total_revenue += txn["Quantity"] * txn["UnitPrice"]

    return round(total_revenue, 2)

## defining function for region wise sales

def region_wise_sales(transactions):
    """
    Analyzes sales by region

    Returns: dictionary with region statistics
    """

    region_data = {}
    total_sales = 0.0

    for txn in transactions:
        region = txn["Region"]
        amount = txn["Quantity"] * txn["UnitPrice"]
        total_sales += amount

        if region not in region_data:
            region_data[region] = {
                "total_sales": 0.0,
                "transaction_count": 0
            }

        region_data[region]["total_sales"] += amount
        region_data[region]["transaction_count"] += 1

    # Calculate percentages
    for region in region_data:
        percentage = (region_data[region]["total_sales"] / total_sales) * 100
        region_data[region]["percentage"] = round(percentage, 2)

    # Sort by total_sales descending
    sorted_regions = dict(
        sorted(
            region_data.items(),
            key=lambda x: x[1]["total_sales"],
            reverse=True
        )
    )

    return sorted_regions

## defining function for top selling products

def top_selling_products(transactions, n=5):
    """
    Finds top n products by total quantity sold

    Returns: list of tuples
    (ProductName, TotalQuantity, TotalRevenue)
    """

    product_data = {}

    for txn in transactions:
        product = txn["ProductName"]
        quantity = txn["Quantity"]
        revenue = txn["Quantity"] * txn["UnitPrice"]

        if product not in product_data:
            product_data[product] = {
                "quantity": 0,
                "revenue": 0.0
            }

        product_data[product]["quantity"] += quantity
        product_data[product]["revenue"] += revenue

    result = [
        (product, data["quantity"], round(data["revenue"], 2))
        for product, data in product_data.items()
    ]

    # Sort by TotalQuantity descending
    result.sort(key=lambda x: x[1], reverse=True)

    return result[:n]

# defining function for customer analysis

def customer_analysis(transactions):
    """
    Analyzes customer purchase patterns

    Returns: dictionary of customer statistics
    """

    customer_data = {}

    for txn in transactions:
        customer = txn["CustomerID"]
        amount = txn["Quantity"] * txn["UnitPrice"]
        product = txn["ProductName"]

        if customer not in customer_data:
            customer_data[customer] = {
                "total_spent": 0.0,
                "purchase_count": 0,
                "products": set()
            }

        customer_data[customer]["total_spent"] += amount
        customer_data[customer]["purchase_count"] += 1
        customer_data[customer]["products"].add(product)

    # Final formatting
    result = {}

    for customer, data in customer_data.items():
        avg_order_value = data["total_spent"] / data["purchase_count"]

        result[customer] = {
            "total_spent": round(data["total_spent"], 2),
            "purchase_count": data["purchase_count"],
            "avg_order_value": round(avg_order_value, 2),
            "products_bought": sorted(list(data["products"]))
        }

    # Sort by total_spent descending
    sorted_result = dict(
        sorted(
            result.items(),
            key=lambda x: x[1]["total_spent"],
            reverse=True
        )
    )

    return sorted_result

## defining function for daily sales trend

def daily_sales_trend(transactions):
    """
    Analyzes sales trends by date

    Returns: dictionary sorted by date
    """

    daily_data = {}

    for txn in transactions:
        date = txn["Date"]
        amount = txn["Quantity"] * txn["UnitPrice"]
        customer = txn["CustomerID"]

        if date not in daily_data:
            daily_data[date] = {
                "revenue": 0.0,
                "transaction_count": 0,
                "customers": set()
            }

        daily_data[date]["revenue"] += amount
        daily_data[date]["transaction_count"] += 1
        daily_data[date]["customers"].add(customer)

    result = {}

    for date in sorted(daily_data.keys()):
        result[date] = {
            "revenue": round(daily_data[date]["revenue"], 2),
            "transaction_count": daily_data[date]["transaction_count"],
            "unique_customers": len(daily_data[date]["customers"])
        }

    return result

## defining function for Peak Sales Day

def find_peak_sales_day(transactions):
    """
    Identifies the date with highest revenue

    Returns: tuple (date, revenue, transaction_count)
    """

    daily = {}

    for txn in transactions:
        date = txn["Date"]
        amount = txn["Quantity"] * txn["UnitPrice"]

        if date not in daily:
            daily[date] = {
                "revenue": 0.0,
                "count": 0
            }

        daily[date]["revenue"] += amount
        daily[date]["count"] += 1

    peak_date = max(daily, key=lambda d: daily[d]["revenue"])

    return (
        peak_date,
        round(daily[peak_date]["revenue"], 2),
        daily[peak_date]["count"]
    )

## defining function for Low performing products

def low_performing_products(transactions, threshold=10):
    """
    Identifies products with low sales

    Returns: list of tuples
    (ProductName, TotalQuantity, TotalRevenue)
    """

    product_data = {}

    for txn in transactions:
        product = txn["ProductName"]
        quantity = txn["Quantity"]
        revenue = txn["Quantity"] * txn["UnitPrice"]

        if product not in product_data:
            product_data[product] = {
                "quantity": 0,
                "revenue": 0.0
            }

        product_data[product]["quantity"] += quantity
        product_data[product]["revenue"] += revenue

    result = [
        (product, data["quantity"], round(data["revenue"], 2))
        for product, data in product_data.items()
        if data["quantity"] < threshold
    ]

    # Sort by TotalQuantity ascending
    result.sort(key=lambda x: x[1])

    return result



