import os
from datetime import datetime
from utils.data_processor import (
    calculate_total_revenue,
    region_wise_sales,
    top_selling_products,
    customer_analysis,
    daily_sales_trend,
    low_performing_products
)


def generate_sales_report(transactions, enriched_transactions, output_file="output/sales_report.txt"):
    """
    Generates a comprehensive formatted text report
    """

    # === CODES UPDATED ===
    # Ensure output directory exists before writing the report
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    # === CODES UPDATED ===

    with open(output_file, "w", encoding="utf-8") as file:

        # ==================================================
        # 1. HEADER
        # ==================================================
        file.write("SALES ANALYTICS REPORT\n")
        file.write("=" * 40 + "\n")
        file.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        file.write(f"Records Processed: {len(transactions)}\n")
        file.write("=" * 40 + "\n\n")

        # ==================================================
        # 2. OVERALL SUMMARY
        # ==================================================
        total_revenue = calculate_total_revenue(transactions)
        total_txns = len(transactions)
        avg_order_value = total_revenue / total_txns if total_txns else 0

        dates = sorted(t["Date"] for t in transactions)

        file.write("OVERALL SUMMARY\n")
        file.write("-" * 40 + "\n")
        file.write(f"Total Revenue      : ₹{total_revenue:,.2f}\n")
        file.write(f"Total Transactions : {total_txns}\n")
        file.write(f"Average Order Value: ₹{avg_order_value:,.2f}\n")
        file.write(f"Date Range         : {dates[0]} to {dates[-1]}\n\n")

        # ==================================================
        # 3. REGION-WISE PERFORMANCE
        # ==================================================
        region_data = region_wise_sales(transactions)

        file.write("REGION-WISE PERFORMANCE\n")
        file.write("-" * 40 + "\n")
        file.write(f"{'Region':<10}{'Sales':>15}{'% of Total':>15}{'Txns':>10}\n")

        for region, stats in region_data.items():
            file.write(
                f"{region:<10}"
                f"₹{stats['total_sales']:>14,.2f}"
                f"{stats['percentage']:>14.2f}%"
                f"{stats['transaction_count']:>10}\n"
            )
        file.write("\n")

        # ==================================================
        # 4. TOP 5 PRODUCTS
        # ==================================================
        top_products = top_selling_products(transactions, n=5)

        file.write("TOP 5 PRODUCTS\n")
        file.write("-" * 40 + "\n")
        file.write(f"{'Rank':<5}{'Product':<20}{'Qty':>6}{'Revenue':>12}\n")

        for i, (product, qty, revenue) in enumerate(top_products, 1):
            file.write(f"{i:<5}{product:<20}{qty:>6}₹{revenue:>11,.2f}\n")
        file.write("\n")

        # ==================================================
        # 5. TOP 5 CUSTOMERS
        # ==================================================
        customers = customer_analysis(transactions)

        file.write("TOP 5 CUSTOMERS\n")
        file.write("-" * 40 + "\n")
        file.write(f"{'Rank':<5}{'Customer':<10}{'Spent':>12}{'Orders':>10}\n")

        for i, (cust, stats) in enumerate(list(customers.items())[:5], 1):
            file.write(
                f"{i:<5}{cust:<10}"
                f"₹{stats['total_spent']:>11,.2f}"
                f"{stats['purchase_count']:>10}\n"
            )
        file.write("\n")

        # ==================================================
        # 6. DAILY SALES TREND
        # ==================================================
        daily_data = daily_sales_trend(transactions)

        file.write("DAILY SALES TREND\n")
        file.write("-" * 40 + "\n")
        file.write(f"{'Date':<12}{'Revenue':>12}{'Txns':>8}{'Customers':>12}\n")

        for date, stats in daily_data.items():
            file.write(
                f"{date:<12}"
                f"₹{stats['revenue']:>11,.2f}"
                f"{stats['transaction_count']:>8}"
                f"{stats['unique_customers']:>12}\n"
            )
        file.write("\n")

        # ==================================================
        # 7. PRODUCT PERFORMANCE ANALYSIS
        # ==================================================
        low_products = low_performing_products(transactions)

        file.write("PRODUCT PERFORMANCE ANALYSIS\n")
        file.write("-" * 40 + "\n")

        if low_products:
            file.write("Low Performing Products:\n")
            for product, qty, revenue in low_products:
                file.write(f"- {product} | Qty: {qty} | Revenue: ₹{revenue:,.2f}\n")
        else:
            file.write("No low-performing products found.\n")
        file.write("\n")

        # ==================================================
        # 8. API ENRICHMENT SUMMARY
        # ==================================================
        matched = [t for t in enriched_transactions if t["API_Match"]]
        unmatched = [t for t in enriched_transactions if not t["API_Match"]]

        success_rate = (len(matched) / len(enriched_transactions)) * 100 if enriched_transactions else 0

        file.write("API ENRICHMENT SUMMARY\n")
        file.write("-" * 40 + "\n")
        file.write(f"Total Enriched Records : {len(enriched_transactions)}\n")
        file.write(f"Successfully Enriched  : {len(matched)}\n")
        file.write(f"Failed Enrichment      : {len(unmatched)}\n")
        file.write(f"Success Rate           : {success_rate:.2f}%\n\n")

        if unmatched:
            file.write("Products Not Enriched:\n")
            for t in unmatched:
                file.write(f"- {t['ProductID']} ({t['ProductName']})\n")
