import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
import os
from dotenv import load_dotenv
import plotly.express as px

# Loading Environment Variables
load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")

# Securing the Database Connection with Pooling
@st.cache_resource
def init_connection():
    return create_engine(
        DATABASE_URL,
        pool_size=5,
        max_overflow=10
    )

engine = init_connection()

# Fetch the Data with Caching
@st.cache_data(ttl=600) 
def get_data(query):
    with engine.connect() as conn:
        df = pd.read_sql(query, conn)
    return df

# DASHBOARD UI
st.set_page_config(page_title="Customer Analytics", layout="wide")
st.title("👥 Customer Analytics Dashboard")

try:
    data = get_data("SELECT * FROM customers LIMIT 1000")
   
    unique_regions = data['region'].dropna().unique() 
    selected_region = st.selectbox("Select a Region to filter by:", unique_regions)

    filtered_data = data[data['region'] == selected_region]

    st.subheader(f"Customer Data for: {selected_region}")
    st.dataframe(filtered_data[['customer_id', 'full_name', 'email', 'status', 'join_date']].tail())

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Customer Status")
        fig_status = px.histogram(
            filtered_data, 
            x='status', 
            title=f"Status Distribution in {selected_region}",
            color='status'
        )
        st.plotly_chart(fig_status, use_container_width=True)

    with col2:
        st.subheader("Gender Breakdown")
        fig_gender = px.pie(
            filtered_data, 
            names='gender', 
            title=f"Gender Ratio in {selected_region}",
            hole=0.4 # Makes it a donut chart!
        )
        st.plotly_chart(fig_gender, use_container_width=True)

except Exception as e:
    st.error(f"Error connecting to the database or fetching data: {e}")