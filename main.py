from utils.report_generator import generate_sales_report
from utils.file_handler import read_sales_data
from utils.data_processor import (
    parse_transactions,
    calculate_total_revenue,
    region_wise_sales,
    top_selling_products,
    customer_analysis,
    daily_sales_trend,
    find_peak_sales_day,
    low_performing_products
)
from utils.data_validator import validate_and_filter
from utils.api_handler import (
    fetch_all_products,
    create_product_mapping,
    enrich_sales_data,
    save_enriched_data
)


def main():
    print("=== SALES ANALYTICS SYSTEM STARTED ===\n")

    # --------------------------------------------------
    # Read Raw Sales Data
    # --------------------------------------------------
    raw_lines = read_sales_data("data/sales_data.txt")
    print(f"Raw lines read (excluding header): {len(raw_lines)}")

    # --------------------------------------------------
    # Parse & Clean Data
    # --------------------------------------------------
    parsed_transactions = parse_transactions(raw_lines)
    print(f"Total records parsed: {len(parsed_transactions)}")

    # --------------------------------------------------
    # Validate & Filter
    # --------------------------------------------------
    valid_transactions, invalid_count, summary = validate_and_filter(parsed_transactions)

    print("\n--- Data Validation Summary ---")
    print(f"Invalid records removed: {invalid_count}")
    print(f"Valid records after cleaning: {len(valid_transactions)}")

    # --------------------------------------------------
    # Data Processing
    # --------------------------------------------------
    total_revenue = calculate_total_revenue(valid_transactions)
    print(f"\nTotal Revenue: {total_revenue}")

    region_summary = region_wise_sales(valid_transactions)
    print("\nRegion-wise Sales Summary:")
    for region, stats in region_summary.items():
        print(region, stats)

    top_products = top_selling_products(valid_transactions)
    print("\nTop Selling Products:")
    for product in top_products:
        print(product)

    customers = customer_analysis(valid_transactions)
    print("\nTop Customers:")
    for cust, stats in list(customers.items())[:3]:
        print(cust, stats)

    peak_day = find_peak_sales_day(valid_transactions)
    print("\nPeak Sales Day:", peak_day)

    low_products = low_performing_products(valid_transactions)
    print("\nLow Performing Products:")
    for p in low_products:
        print(p)

    # --------------------------------------------------
    # Fetch Products from DummyJSON API
    # --------------------------------------------------
    print("\n=== FETCHING PRODUCTS FROM API ===")
    api_products = fetch_all_products()

    # --------------------------------------------------
    # Create Product Mapping
    # --------------------------------------------------
    product_mapping = create_product_mapping(api_products)
    print(f"Product mapping created for {len(product_mapping)} API products")

    # --------------------------------------------------
    # Enrich Sales Data
    # --------------------------------------------------
    enriched_transactions = enrich_sales_data(valid_transactions, product_mapping)

    # --------------------------------------------------
    # Validate Enrichment Count
    # --------------------------------------------------
    matched_count = sum(1 for t in enriched_transactions if t["API_Match"])
    unmatched_count = sum(1 for t in enriched_transactions if not t["API_Match"])

    print("\n--- API Enrichment Validation ---")
    print(f"API_Match = True  : {matched_count}")
    print(f"API_Match = False : {unmatched_count}")
    print(f"Total Enriched Records: {len(enriched_transactions)}")

    # --------------------------------------------------
    # Save Enriched Data to File
    # --------------------------------------------------
    save_enriched_data(enriched_transactions)

    # ==================================================
    
    # Generate Text Report
    # ==================================================
    generate_sales_report(
        transactions=valid_transactions,
        enriched_transactions=enriched_transactions
    )
    

    print("\nSales report generated: output/sales_report.txt")
    print("\n=== SALES ANALYTICS SYSTEM COMPLETED SUCCESSFULLY ===")


if __name__ == "__main__":
    main()
