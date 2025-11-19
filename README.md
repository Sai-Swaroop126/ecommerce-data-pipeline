📦 End-to-End eCommerce Data Pipeline
Python • SQL • BigQuery • Looker Studio • Data Engineering Project

This project is a complete end-to-end data engineering pipeline that processes raw eCommerce data, transforms it using Python, loads it into Google BigQuery for analysis, performs RFM segmentation + business insights using SQL, and visualizes everything with an interactive Looker Studio dashboard.

ecommerce-data-pipeline/
│
├── data/
│   └── samples/                     # Sample clean datasets
│
├── scripts/
│   ├── extract_data.py              # Extract raw CSV data
│   └── clean_transform_pipeline.py  # Clean & transform logic
│
├── sql/
│   ├── basic_business_insights.sql  # Business KPIs & trends
│   ├── query_for_rfmscore.sql       # RFM scoring logic
│   ├── rfm.sql                      # Recency & frequency queries
│   └── rfm_table.sql                # Combined RFM table
│
├── LockerStudio.pdf                 # Dashboard export
│
├── clean_customers.csv
├── clean_orders.csv
├── clean_products.csv
│
├── customers.csv
├── orders.csv
├── products.csv
│
└── README.md                        # Final documentation

🎯 Project Goal

Build a fully automated eCommerce analytics pipeline capable of producing meaningful business insights and customer segmentation.

🔄 Pipeline Steps
Step	Description
1. Extract	Python reads raw CSVs (customers, products, orders).
2. Transform	Handles nulls, formats dates, standardizes columns.
3. Load	Cleaned data is uploaded into Google BigQuery.
4. SQL Analysis	Business queries + RFM segmentation done in BigQuery.
5. Visualization	Insights visualized using Looker Studio.
🛠 Technologies Used
Tool	Usage
Python	Data extraction & transformation
Pandas	Cleaning and preprocessing
Google BigQuery	SQL analytics & data warehouse
Looker Studio	Dashboards & data visualization
GitHub	Version control
VS Code	Development environment
🔍 BigQuery SQL – Highlights
📈 Revenue Insights

Total revenue

Total orders

Monthly revenue trends

State-wise revenue

Total items sold

Unique customers

Top-selling products

🎯 RFM Segmentation

Calculated using:

Recency → Days since last purchase

Frequency → Total orders

Monetary → Total value spent

RFM scores are calculated using quantile scoring.

🧩 Customer Segments

⭐ Premium

👍 Loyal

💤 About-to-Sleep

⚠ At-Risk

❌ Lost

👉 All SQL queries are available inside the sql/ folder.

📊 Looker Studio Dashboard

The interactive dashboard includes:

📈 Revenue metrics

👥 Customer growth

🛒 Order trends

🎯 RFM segmentation visuals

🗺️ State-wise distribution

📅 Monthly insights

These visuals help businesses understand:

Premium customer behavior

Declining segments

Buying patterns

Seasonal trends

📄 Dashboard PDF: LockerStudio.pdf

🏅 Certifications
Google Cloud Skill Badge — Introduction to Data Engineering

Hands-on labs completed:

BigQuery basics

Data modeling

ETL workflows

Query optimization

Cloud storage & ingestion

BigQuery analytics end-to-end

This certification validates foundational cloud-based data engineering skills.

✅ Project Status

✔ Completed successfully
✔ Ready for portfolio/interviews
✔ Demonstrates end-to-end data engineering skills




