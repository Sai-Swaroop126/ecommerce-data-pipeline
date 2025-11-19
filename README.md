📦 End-to-End eCommerce Data Pipeline
Python • SQL • BigQuery • Looker Studio Dashboard

This project is an end-to-end data engineering pipeline that takes raw eCommerce data, processes it, loads it into BigQuery, performs analytical SQL queries (RFM segmentation + business insights), and visualizes everything using Looker Studio.

ecommerce-data-pipeline/
│
├── data/
│   ├── raw/                    # Raw input CSV files  
│   └── samples/                # Sample clean datasets  
│
├── scripts/
│   ├── extract_data.py         # Extract CSV data  
│   └── clean_transform_pipeline.py   # Clean & transform logic  
│
├── sql/
│   ├── basic_business_insights.sql   # Revenue, orders, monthly trends  
│   ├── query_for_rfmscore.sql        # RFM score logic  
│   ├── rfm.sql                        # Frequency, recency tables  
│   └── rfm_table.sql                  # Final RFM combined table  
│
├── clean_customers.csv  
├── clean_orders.csv  
├── clean_products.csv  
├── customers.csv  
├── orders.csv  
├── products.csv  
│
├── LookerStudio.pdf            # Dashboard screenshots  


Goal:

Build a complete data pipeline that can generate insights for an eCommerce business.

✔ Steps involved
Step	Description
1. Extract	Python reads raw CSV data (customers, orders, products).
2. Transform	Cleans & standardizes data (dates, nulls, formatting).
3. Load	Uploads cleaned data into Google BigQuery.
4. SQL Analysis	Business queries & RFM segmentation performed in BigQuery.
5. Visualization	Interactive dashboard created in Looker Studio.



Python	Extract & transform data
Pandas	Data cleaning
Google BigQuery	SQL analytics & data warehouse
Looker Studio	Dashboard & visualizations
GitHub	Version control
VS Code	Development environment


🔍 BigQuery SQL (Highlights)
🔹 Revenue Insights

Total revenue

Total orders

Unique customers

Monthly revenue trend

Total items sold

🔹 RFM Segmentation

Recency (days since last purchase)

Frequency (orders count)

Monetary (total order value)

RFM score using quantile scoring

Customer segmentation:

⭐ Premium

👍 Loyal

💤 About-to-Sleep

⚠ At-Risk

❌ Lost

Your SQL scripts for these are stored in the sql/ folder.

📊 Looker Studio Dashboard

You created a complete dashboard that includes:

Revenue metrics

Orders analysis

Customer growth

RFM segmentation visuals

State-wise data distributions

Monthly trends
│
├── README.md  
└── .gitignore  
