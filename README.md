# 🏦 Fintech Data Warehouse & Analytics Engine

[![Python](https://img.shields.io/badge/Python-3.11-blue.svg)](https://www.python.org/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Neon-336791.svg)](https://neon.tech/)
[![dbt](https://img.shields.io/badge/dbt-Data_Build_Tool-FF694B.svg)](https://www.getdbt.com/)
[![Streamlit](https://img.shields.io/badge/Streamlit-App-FF4B4B.svg)](https://streamlit.io/)
[![Deployed on Render](https://img.shields.io/badge/Deployed-Render-46E3B7.svg)](https://render.com/)

**Live Dashboard:** https://fintech-customer-dashboard.onrender.com 
**Video Demo:** [Insert Video URL Here]

## 📌 Project Overview
This project is an end-to-end Data Engineering pipeline designed to process, model, and visualize financial transaction and customer demographic data. It utilizes a modern data stack to extract raw operational data, transform it via a structured staging and modeling process, and serve it to a live, interactive Business Intelligence dashboard.

## 🗄️ Database Architecture & Data Modeling
A core component of this project was transforming highly normalized transactional data into a denormalized Star Schema optimized for fast analytical queries.

### 1. Raw Data Source (OLTP)
The initial data ingestion follows a 3rd Normal Form (3NF) relational structure to ensure data integrity during capture.

![Raw Data Schema](ERD_IMAGE.png)

### 2. Analytical Data Warehouse (OLAP)
Using dbt (Data Build Tool), the raw tables were transformed and modeled into a dimensional Star Schema. This structure significantly reduces SQL join complexity and powers the live Streamlit dashboard.

![Dimensional Star Schema](Structure%20.jpg)

## 🏗️ Architecture & Tech Stack

* **Data Ingestion:** Custom Python scripts extract raw data and load it into the data warehouse.
* **Storage / Data Warehouse:** **Neon (Serverless PostgreSQL)** is used for high-performance, cloud-native data storage.
* **Data Transformation:** **dbt (Data Build Tool)** handles the ELT process, transforming raw tables into clean, tested `stg_` (staging) views, and ultimately into `dim_` (dimension) and `fct_` (fact) tables.
* **Orchestration:** **GitHub Actions** automates and orchestrates the dbt transformation runs.
* **Presentation Layer:** A **Streamlit** Python application serves as the BI Dashboard, querying the modeled data dynamically.
* **Cloud Deployment:** The frontend application is continuously deployed and hosted on **Render**.

## 📊 Dashboard Features
The live Streamlit application features a multi-page architecture:
1. **📇 Customer Directory:** A searchable interface querying the `dim_customers` dimension table.
2. **💰 Financial Overview:** Interactive time-series and distribution visualizations driven by the `fct_transactions` fact table, including dynamic date-range filtering and KPI scorecards.
3. **🚀 Advanced Analytics:** Automated aggregation models identifying top Lifetime Value (LTV) customers.

## ⚙️ Local Setup Instructions

To run this project locally, follow these steps:

**1. Clone the repository:**
```bash
git clone https://github.com/yourusername/EAS550_FintechData.git
cd EAS550_FintechData
```

**2. Install dependencies:**
```bash
pip install -r requirements.txt
```

**3. Configure Environment Variables:**
Create a `.env` file in the root directory and add your Neon PostgreSQL connection string:

```
DATABASE_URL=postgresql://[user]:[password]@[host]/[database]?sslmode=require
```

**4. Run the Streamlit App:**
```bash
streamlit run app.py
```

## 🗄️ Repository Structure
- `app.py`: Main Streamlit application and UI routing.
- `models/`: Contains all dbt SQL models (`stg_`, `dim_`, `fct_`).
- `dbt_project.yml`: Configuration file for the dbt pipeline.
- `schema.sql`: Initial DDL scripts for the database structure.
- `requirements.txt`: Python dependencies for deployment.
- `.github/workflows/`: CI/CD orchestration files.