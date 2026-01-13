def validate_and_filter(transactions, region=None, min_amount=None, max_amount=None):
    """
    Validates transactions and applies optional filters

    Returns:
    (valid_transactions, invalid_count, filter_summary)
    """

    valid_transactions = []
    invalid_count = 0

    total_input = len(transactions)
    filtered_by_region = 0
    filtered_by_amount = 0

    # Display available regions
    available_regions = sorted(
        set(t["Region"] for t in transactions if t.get("Region"))
    )
    print("Available Regions:", available_regions)

    # Display transaction amount range
    amounts = [t["Quantity"] * t["UnitPrice"] for t in transactions]
    print(f"Transaction Amount Range: {min(amounts)} - {max(amounts)}")

    for txn in transactions:
        try:
            # Validation rules
            if txn["Quantity"] <= 0:
                raise ValueError
            if txn["UnitPrice"] <= 0:
                raise ValueError
            if not txn["TransactionID"].startswith("T"):
                raise ValueError
            if not txn["ProductID"].startswith("P"):
                raise ValueError
            if not txn["CustomerID"].startswith("C"):
                raise ValueError
            if not txn["Region"]:
                raise ValueError

            amount = txn["Quantity"] * txn["UnitPrice"]

            # Region filter
            if region and txn["Region"] != region:
                filtered_by_region += 1
                continue

            # Amount filters
            if min_amount and amount < min_amount:
                filtered_by_amount += 1
                continue

            if max_amount and amount > max_amount:
                filtered_by_amount += 1
                continue

            valid_transactions.append(txn)

        except Exception:
            invalid_count += 1

    filter_summary = {
        "total_input": total_input,
        "invalid": invalid_count,
        "filtered_by_region": filtered_by_region,
        "filtered_by_amount": filtered_by_amount,
        "final_count": len(valid_transactions)
    }

    return valid_transactions, invalid_count, filter_summary
