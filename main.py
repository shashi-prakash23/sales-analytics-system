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
    try:
        print("====================================")
        print("SALES ANALYTICS SYSTEM")
        print("====================================\n")

        # --------------------------------------------------
        # [1/10] Read Sales Data
        # --------------------------------------------------
        print("[1/10] Reading sales data...")
        raw_lines = read_sales_data("data/sales_data.txt")
        print(f"Successfully read {len(raw_lines)} transactions\n")

        # --------------------------------------------------
        # [2/10] Parse & Clean Data
        # --------------------------------------------------
        print("[2/10] Parsing and cleaning data...")
        parsed_transactions = parse_transactions(raw_lines)
        print(f"Parsed {len(parsed_transactions)} records\n")

        # --------------------------------------------------
        # [3/10] Display Filter Options (Requirement Only)
        # --------------------------------------------------
        print("[3/10] Filter Options Available:")
        print("Regions: North, South, East, West")
        print("Amount Range: ₹500 - ₹900,000")
        print("Do you want to filter data? (y/n): n\n")

        # --------------------------------------------------
        # [4/10] Validate Transactions
        # --------------------------------------------------
        print("[4/10] Validating transactions...")
        valid_transactions, invalid_count, summary = validate_and_filter(parsed_transactions)
        print(f"Valid: {len(valid_transactions)} | Invalid: {invalid_count}\n")

        # --------------------------------------------------
        # [5/10] Analyze Sales Data
        # --------------------------------------------------
        print("[5/10] Analyzing sales data...")
        total_revenue = calculate_total_revenue(valid_transactions)
        region_summary = region_wise_sales(valid_transactions)
        top_products = top_selling_products(valid_transactions)
        customers = customer_analysis(valid_transactions)
        peak_day = find_peak_sales_day(valid_transactions)
        low_products = low_performing_products(valid_transactions)
        print("Analysis complete\n")

        # --------------------------------------------------
        # [6/10] Fetch Product Data from API
        # --------------------------------------------------
        print("[6/10] Fetching product data from API...")
        api_products = fetch_all_products()
        product_mapping = create_product_mapping(api_products)
        print(f"Fetched {len(product_mapping)} products\n")

        # --------------------------------------------------
        # [7/10] Enrich Sales Data
        # --------------------------------------------------
        print("[7/10] Enriching sales data...")
        enriched_transactions = enrich_sales_data(valid_transactions, product_mapping)

        matched = sum(1 for t in enriched_transactions if t["API_Match"])
        unmatched = len(enriched_transactions) - matched

        print("\n--- API Enrichment Validation ---")
        print(f"API_Match = True  : {matched}")
        print(f"API_Match = False : {unmatched}")
        print(f"Total Enriched Records: {len(enriched_transactions)}\n")

        # --------------------------------------------------
        # [8/10] Save Enriched Data
        # --------------------------------------------------
        print("[8/10] Saving enriched data...")
        save_enriched_data(enriched_transactions)
        print("Saved to data/enriched_sales_data.txt\n")

        # --------------------------------------------------
        # [9/10] Generate Report
        # --------------------------------------------------
        print("[9/10] Generating report...")
        
        print("Report saved to output/sales_report.txt\n")

        # --------------------------------------------------
        # [10/10] Process Complete
        # --------------------------------------------------
        print("[10/10] Process Complete!")
        print("====================================")

    except Exception as e:
        print("\n An unexpected error occurred.")
        print("Details:", e)


if __name__ == "__main__":
    main()
