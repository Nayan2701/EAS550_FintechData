import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
import os
from dotenv import load_dotenv
import plotly.express as px

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")

@st.cache_resource
def init_connection():
    return create_engine(
        DATABASE_URL,
        pool_size=5,
        max_overflow=10
    )

engine = init_connection()

@st.cache_data(ttl=600) 
def get_data(query):
    with engine.connect() as conn:
        df = pd.read_sql(query, conn)
    return df

st.set_page_config(page_title="Enterprise Fintech Analytics", page_icon="📊", layout="wide")

with st.sidebar:
    st.title("⚙️ Fintech Data OS")
    st.markdown("Select a module below:")
    page = st.radio("Go to:", ["📇 Customer Directory", "💰 Financial Overview", "🚀 Advanced Analytics"])
    st.markdown("---")
    st.success("🟢 Live Connection: Neon DB")
    st.info("Pipeline: dbt Models ➔ PostgreSQL ➔ Streamlit")


# PAGE 1: CUSTOMER DIRECTORY

if page == "📇 Customer Directory":
    st.title("📇 Customer Directory")
    st.markdown("Search and view customer records directly from the dimension table (`dim_customers`).")
    
    try:
        cust_data = get_data("SELECT * FROM dim_customers")
        
        # UI Polish: Put the search bar in a stylized container
        with st.container():
            search_query = st.text_input("🔍 Search by Name or Email:", "")
        
        if search_query:
            mask = (
                cust_data['full_name'].str.contains(search_query, case=False, na=False) |
                cust_data['email'].str.contains(search_query, case=False, na=False)
            )
            filtered_cust = cust_data[mask]
        else:
            filtered_cust = cust_data

        st.caption(f"Displaying {len(filtered_cust)} matching records.")
        st.dataframe(filtered_cust[['customer_id', 'full_name', 'email']], use_container_width=True, hide_index=True)

    except Exception as e:
        st.error(f"Error loading Customer data: {e}")


# PAGE 2: FINANCIAL OVERVIEW

elif page == "💰 Financial Overview":
    st.title("💰 Financial Overview")
    
    try:
        txn_data = get_data("SELECT * FROM fct_transactions")
        txn_data['transaction_date'] = pd.to_datetime(txn_data['transaction_date'])
        
        min_date = txn_data['transaction_date'].min().date()
        max_date = txn_data['transaction_date'].max().date()
        
        # Date Filter
        date_selection = st.date_input("🗓️ Filter Date Range", value=(min_date, max_date), min_value=min_date, max_value=max_date)
        
        if len(date_selection) == 2:
            start_date, end_date = date_selection
            mask = (txn_data['transaction_date'].dt.date >= start_date) & (txn_data['transaction_date'].dt.date <= end_date)
            filtered_txn = txn_data[mask]
        else:
            filtered_txn = txn_data

        # --- NEW: KPI SCORECARDS ---
        st.markdown("### Top-Level Metrics")
        kpi1, kpi2, kpi3 = st.columns(3)
        
        total_volume = filtered_txn['amount'].sum()
        avg_txn_size = filtered_txn['amount'].mean()
        total_txns = len(filtered_txn)
        
        kpi1.metric(label="Total Processed Volume", value=f"${total_volume:,.2f}")
        kpi2.metric(label="Average Transaction", value=f"${avg_txn_size:,.2f}")
        kpi3.metric(label="Total Transactions", value=f"{total_txns:,}")
        
        st.markdown("---")

       
        tab1, tab2 = st.tabs(["📈 Visualizations", "🗄️ Raw Data Explorer"])
        
        with tab1:
            col1, col2 = st.columns(2)
            
            with col1:
                daily_vol = filtered_txn.groupby('transaction_date')['amount'].sum().reset_index()
                # Added an area chart instead of a line chart for a more "fintech" feel
                fig_area = px.area(daily_vol, x='transaction_date', y='amount', title="Daily Transaction Volume ($)")
                st.plotly_chart(fig_area, use_container_width=True)
                
            with col2:
                fig_hist = px.histogram(filtered_txn, x='amount', title="Transaction Size Distribution", nbins=40, color_discrete_sequence=['#1f77b4'])
                st.plotly_chart(fig_hist, use_container_width=True)
                
        with tab2:
            st.dataframe(filtered_txn, use_container_width=True, hide_index=True)

    except Exception as e:
        st.error(f"Error loading Transaction data: {e}")


# PAGE 3: ADVANCED ANALYTICS (NEW)

elif page == "🚀 Advanced Analytics":
    st.title("🚀 Advanced Analytics")
    st.markdown("Deep dive into customer spending behaviors and dataset architecture.")
    
    try:
        txn_data = get_data("SELECT * FROM fct_transactions")
        
        col1, col2 = st.columns([2, 1]) # Makes the first column twice as wide
        
        with col1:
            st.subheader("🏆 Top 10 Customers by Lifetime Value (LTV)")
            top_spenders = txn_data.groupby('customer_id')['amount'].sum().reset_index()
            top_spenders = top_spenders.sort_values(by='amount', ascending=False).head(10)
            
            top_spenders['amount'] = top_spenders['amount'].apply(lambda x: f"${x:,.2f}")
            
            st.dataframe(top_spenders, use_container_width=True, hide_index=True)
            
        with col2:
            st.subheader("💡 Architecture Insights")
            st.info("""
            **Data Pipeline Stats:**
            - **Ingestion:** Raw Python scripts
            - **Storage:** Neon Serverless Postgres
            - **Transformation:** dbt (Data Build Tool)
            - **Orchestration:** GitHub Actions
            - **Presentation:** Streamlit
            """)
            
            with st.expander("View Data Dictionary"):
                st.write("**Fact Table (`fct_transactions`):** Contains immutable transactional events.")
                st.write("**Dim Table (`dim_customers`):** Contains slowly changing dimension (SCD) customer demographics.")
                
    except Exception as e:
        st.error(f"Error loading analytics: {e}")