import streamlit as st
import pandas as pd
import pandas_gbq
from google.oauth2 import service_account
from google.cloud import bigquery

st.set_page_config(page_title="Attribution Model Testing",page_icon="🧑‍🚀",layout="wide")

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

if __name__ == '__main__':
    st.write("Test")

