import pandas as pd
import requests
from datetime import datetime
import time
import streamlit as st

# Function to fetch ACAPS data
@st.cache_data
def fetch_acaps_data(country):
    # Post credentials to get an authentication token
    credentials = {
        "username": st.secrets["acaps"]["username"],  
        "password": st.secrets["acaps"]["password"]  
    }
    auth_token_response = requests.post("https://api.acaps.org/api/v1/token-auth/", credentials)
    auth_token = auth_token_response.json()['token']

    # Pull data from ACAPS API, loop through the pages, and append to a pandas DataFrame
    df_list = []
    request_url = f"https://api.acaps.org/api/v1/risk-list/?country={country}"  
    last_request_time = datetime.now()
    while True:
        # Wait to avoid throttling
        while (datetime.now() - last_request_time).total_seconds() < 1:
            time.sleep(0.1)

        # Make the request
        response = requests.get(request_url, headers={"Authorization": "Token %s" % auth_token})
        last_request_time = datetime.now()
        response = response.json()

        # Append to a list of DataFrames
        df_list.append(pd.DataFrame(response["results"]))

        # Loop to the next page; if we are on the last page, break the loop
        if ("next" in response.keys()) and (response["next"] is not None):
            request_url = response["next"]
        else:
            break

    # Concatenate all DataFrames in the list
    df = pd.concat(df_list, ignore_index=True)

    return df