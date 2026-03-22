import pandas as pd
from sqlalchemy import create_engine

DATABASE_URL = "postgresql://neondb_owner:npg_4wUkEueKrlT0@ep-empty-paper-anqv2oi6-pooler.c-6.us-east-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require"

engine = create_engine(
    DATABASE_URL, 
    pool_size=5, 
    max_overflow=10, 
    pool_timeout=30,
    pool_recycle=1800 
)

def load_idempotent(df, table_name, unique_col):
    print(f"Checking existing records in '{table_name}' table...")
    try:
        existing_ids = pd.read_sql(f"SELECT {unique_col} FROM {table_name}", engine)
        new_records = df[~df[unique_col].isin(existing_ids[unique_col])]
    except Exception:
        new_records = df

    if not new_records.empty:
        print(f"Inserting {len(new_records)} new rows into '{table_name}'...")
        new_records.to_sql(table_name, engine, if_exists='append', index=False)
        print(f"{table_name} updated successfully.\n")
    else:
        print(f" No new records found for {table_name}. Skipped.\n")

def process_and_ingest():

    df_customers = pd.read_csv('/Users/nayanpaliwal/Desktop/Spring-2026/data_query/FINTECH_DATA/EAS550_FintechData/archive/DimCustomer.csv')
    df_customers = df_customers.rename(columns={
        'CustomerID': 'customer_id', 'FullName': 'full_name', 'DOB': 'dob',
        'Gender': 'gender', 'Region': 'region', 'Email': 'email',
        'Status': 'status', 'JoinDate': 'join_date'
    })
    df_customers['dob'] = pd.to_datetime(df_customers['dob'], format='mixed').dt.date
    df_customers['join_date'] = pd.to_datetime(df_customers['join_date'], format='mixed').dt.date
    load_idempotent(df_customers, 'customers', 'customer_id')

    df_accounts = pd.read_csv('/Users/nayanpaliwal/Desktop/Spring-2026/data_query/FINTECH_DATA/EAS550_FintechData/archive/DimAccount.csv')
    df_accounts = df_accounts.rename(columns={
        'AccountID': 'account_id', 'CustomerID': 'customer_id',
        'AccountType': 'account_type', 'Balance': 'balance'
    })
    df_accounts = df_accounts[['account_id', 'customer_id', 'account_type', 'balance']]
    load_idempotent(df_accounts, 'accounts', 'account_id')

    df_products = pd.read_csv('/Users/nayanpaliwal/Desktop/Spring-2026/data_query/FINTECH_DATA/EAS550_FintechData/archive/Dimproduct.txt', sep=None, engine='python')
    df_products = df_products.rename(columns={
        'ProductID': 'product_id', 
        'ProductName': 'product_name', 
        'ProductSubcategoryID': 'product_category'
    })

    df_products = df_products[['product_id', 'product_name', 'product_category']]
    load_idempotent(df_products, 'products', 'product_id')

    df_transactions = pd.read_csv('/Users/nayanpaliwal/Desktop/Spring-2026/data_query/FINTECH_DATA/EAS550_FintechData/archive/FactTransaction.csv')
    df_transactions = df_transactions.rename(columns={
        'TransactionID': 'transaction_id', 'AccountID': 'account_id',
        'ProductID': 'product_id', 'TransactionDate': 'transaction_date',
        'TransactionAmount': 'transaction_amount', 'TransactionType': 'transaction_type',
        'TransactionChannel': 'transaction_channel', 'Status': 'status'
    })
    df_transactions = df_transactions[['transaction_id', 'account_id', 'product_id', 'transaction_date', 'transaction_amount', 'transaction_type', 'transaction_channel', 'status']]
    df_transactions['transaction_date'] = pd.to_datetime(df_transactions['transaction_date'], format='mixed').dt.date
    load_idempotent(df_transactions, 'transactions', 'transaction_id')

    print("All data successfully ingested into Neon PostgreSQL!")

if __name__ == "__main__":
    process_and_ingest()