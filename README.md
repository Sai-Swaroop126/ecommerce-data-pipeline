📦 End-to-End eCommerce Data Pipeline
Python • SQL • BigQuery • Looker Studio • Data Engineering Project

This project is a complete end-to-end data engineering pipeline that processes raw eCommerce data, transforms it using Python, loads it into Google BigQuery for analytics, performs business intelligence + RFM segmentation, and visualizes insights using Looker Studio.

ecommerce-data-pipeline/
│── data/
│   └── samples/                        # Sample clean datasets
│
│── scripts/
│   ├── extract_data.py                 # Extract raw CSV data
│   └── clean_transform_pipeline.py     # Clean & transform logic
│
│── sql/
│   ├── basic_business_insights.sql     # Business KPIs, trends
│   ├── query_for_rfmscore.sql          # RFM scoring logic
│   ├── rfm.sql                         # Recency & frequency tables
│   └── rfm_table.sql                   # Final RFM combined table
│
│── LockerStudio.pdf                    # Dashboard export
│── clean_customers.csv
│── clean_orders.csv
│── clean_products.csv
│── customers.csv
│── orders.csv
│── products.csv
│
└── README.md                           # Final documentation


Project Goal
Build a complete, automated data pipeline capable of producing business insights for an eCommerce company.

Pipeline Steps
Step	Description
1. Extract	Python script reads raw CSVs (customers, orders, products).
2. Transform	Clean & standardize data (nulls, date formats, duplicates).
3. Load	Upload cleaned data into Google BigQuery tables.
4. SQL Analysis	Run business queries + RFM segmentation.
5. Visualization	Build interactive dashboard in Looker Studio.

Technologies Used
Tool	            Purpose
Python     	Extract & transform data
Pandas     	Data cleaning & preprocessing
GoogleBigQuery	SQL analytics & data warehouse
Looker Studio	  Dashboards & visualizations
GitHub         	Version control
VS Code       	Development environment


BigQuery SQL – Highlights
Revenue Insights
Total revenue
Total orders
Monthly revenue trends
Total items sold
Unique customers
Top-selling products
State-wise revenue distribution

🎯 RFM Segmentation

Calculated using:
Recency = Days since last purchase
Frequency = Total orders
Monetary = Total order value
RFM score computed using quantile scoring.

🧩 Customer Segments

 Premium
 Loyal
About-to-Sleep
At-Risk
 Lost

👉 All SQL scripts are available inside the sql/ folder.

📊 Looker Studio Dashboard

The interactive dashboard includes:

📈 Revenue metrics

🛒 Order analysis

👥 Customer growth

🎯 RFM segmentation visuals

🗺️ State-wise customer distribution

📅 Monthly trends

It enables businesses to easily identify:

Premium customers

Declining customer segments

Buying patterns

Long-term trends and seasonality

➡️ Dashboard PDF is included as LockerStudio.pdf in the repository.

Status: Completed Successfully
This project demonstrates skills in data engineering, SQL analytics, ETL pipelines, and dashboard building — suitable for portfolio use and interviews.



🏅 Certifications
Google Cloud Skill Badge — Introduction to Data Engineering
Earned the official Google Cloud skill badge by completing multiple hands-on labs covering:
BigQuery basics
ETL workflows
Data modeling
Storage and querying
Building data pipelines using Google Cloud tools







