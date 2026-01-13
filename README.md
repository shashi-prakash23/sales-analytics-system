# Sales Analytics System

## Assignment 3 – Python Data Analytics Project

This project implements an end-to-end Sales Analytics System using Python.  
It processes raw sales data from a text file, performs data cleaning and validation, conducts business analytics, enriches data using an external API, and generates a comprehensive text-based sales report.

---

## Project Structure

sales-analytics-system/
│
├── main.py
├── README.md
├── requirements.txt
│
├── data/
│   ├── sales_data.txt
│   └── enriched_sales_data.txt
│
├── output/
│   └── sales_report.txt
│
├── utils/
│   ├── __init__.py
│   ├── file_handler.py
│   ├── data_processor.py
│   ├── data_validator.py
│   ├── api_handler.py
│   └── report_generator.py

---

## Functional Overview

### 1. Data Ingestion
- Reads sales_data.txt with encoding handling
- Skips headers and empty lines

### 2. Data Parsing and Cleaning
- Pipe (|) delimited parsing
- Cleans commas from product names and numeric fields
- Converts data into structured dictionaries

### 3. Data Validation
- Validates TransactionID, ProductID, CustomerID formats
- Ensures Quantity and UnitPrice are positive
- Removes invalid records

### 4. Sales Analytics
- Total revenue calculation
- Region-wise sales analysis
- Top-selling products
- Customer purchase analysis
- Daily sales trends
- Peak sales day identification
- Low-performing products

### 5. API Integration
- Fetches product data from DummyJSON API
- Enriches sales records with category, brand, rating
- Flags matched and unmatched records
- Saves enriched data to file

### 6. Report Generation
- Generates a formatted text report
- Includes summaries, analytics, trends, and API enrichment results
- Output saved in output/sales_report.txt

---

## How to Run the Project

### Install Dependencies
```bash
pip install -r requirements.txt
