import streamlit as st
import pandas as pd
import pandas
import pandas_gbq
from google.oauth2 import service_account
from google.cloud import bigquery
from google.cloud import storage
from datetime import datetime, timedelta
import matplotlib.pyplot as plt


st.set_page_config(page_title="Attribution Model Testing",page_icon="🚀",layout="wide")

credentials = service_account.Credentials.from_service_account_info(
          st.secrets["gcp_service_account"]
      )
client = bigquery.Client(credentials=credentials)

def initialize_storage_client():
    credentials = service_account.Credentials.from_service_account_info(
        st.secrets["gcp_service_account"]
    )
    storage_client = storage.Client(credentials=credentials)
    return storage_client

# Use this client for GCS operations
storage_client = initialize_storage_client()

one_year_ago = (datetime.now() - timedelta(days=365)).date()

if __name__ == '__main__':
    st.markdown("<h1 style='text-align: center;'>Attribution Model Testing</h1>", unsafe_allow_html=True)

    if 'full_data' not in st.session_state:
      credentials = service_account.Credentials.from_service_account_info(
          st.secrets["gcp_service_account"]
      )
      client = bigquery.Client(credentials=credentials)
      # Modify the query
      query = f"""
      SELECT * FROM `tipsy-elves-405719.tipsy_elves_agg.tipsy_elves_full_funnel` 
      WHERE Date BETWEEN '{one_year_ago}' AND CURRENT_DATE() """
      st.session_state.full_data = pandas.read_gbq(query, credentials=credentials)

    data = st.session_state.full_data

    grouped_df = data.groupby(['Date', 'Platform']).agg({
        'Cost': 'sum',
        'Conversions': 'sum',
        'Orders__Shopify': 'sum',
        'Revenue': 'sum'
    }).reset_index()

    total_cost = grouped_df['Cost'].sum()

    # Calculate the proportion of each platform's cost
    grouped_df['Cost_Proportion'] = grouped_df['Cost'] / total_cost

    # Attribute conversions based on cost proportion
    grouped_df['Attributed_Conversions'] = grouped_df['Conversions'] * grouped_df['Cost_Proportion']

    # Similarly, attribute revenue based on cost proportion
    grouped_df['Attributed_Revenue'] = grouped_df['Revenue'] * grouped_df['Cost_Proportion']

    st.write("Attribution Analysis")
    fig, ax = plt.subplots()
    grouped_df.plot(kind='bar', x='Platform', y=['Conversions', 'Attributed_Conversions'], ax=ax)
    st.pyplot(fig)




