import streamlit as st
import requests
import pandas as pd
from datetime import datetime, timedelta
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain.prompts import PromptTemplate

def acled_page():
    st.title("ACLED Data Viewer")
    st.divider()

    # Filters Section
    st.write("Filters")

    # First Row with Four Columns
    row1_col1, row1_col2, row1_col3, row1_col4 = st.columns(4)
    with row1_col1:
        country = st.text_input("Country", 
                                value="Nigeria")
    with row1_col2:
        limit = st.number_input("Number of Records", 
                                min_value=1, 
                                max_value=500, 
                                value=50, 
                                step=10)
    with row1_col3:
        today = datetime.today()
        default_start_date = today - timedelta(days=30)
        start_date = st.date_input("Start Date", default_start_date, format="YYYY-MM-DD")
    with row1_col4:
        end_date = st.date_input("End Date", today, format="YYYY-MM-DD")

    event_type_options = [
            'Battles', 'Explosions/Remote violence', 'Violence against civilians',
            'Protests', 'Riots', 'Strategic developments'
        ]
    event_types = st.multiselect("Event Types", event_type_options, default=event_type_options)
    fetch_button = st.button("Fetch Data")

    # Fetch data when the button is clicked
    if fetch_button:
        with st.spinner("Fetching data from ACLED API..."):
            api_key = st.secrets["ACLED_API_KEY"]
            email = st.secrets["ACLED_EMAIL"]
            data = fetch_acled_data(
                api_key=api_key,
                email=email,
                country=country,
                event_types=event_types,
                start_date=start_date,
                end_date=end_date,
                limit=limit
            )
            if data is not None:
                st.success(f"Fetched {len(data[1])} records.")
                st.session_state.acled_data = data
                display_acled_data(data)
            else:
                st.error("Failed to fetch data. Please check your API key, email, and filters.")
    else:
        # If data is already in session_state, display it
        if 'acled_data' in st.session_state:
            data = st.session_state.acled_data
            display_acled_data(data)

@st.cache_data(show_spinner=False)
def fetch_acled_data(api_key, email, country, event_types, start_date, end_date, limit):
    if country == "All":
        base_url = "https://api.acleddata.com/acled/read/?key="+api_key+"&email="+email+"&limit="+str(limit)
    else:
        base_url = "https://api.acleddata.com/acled/read/?key="+api_key+"&email="+email+"&limit="+str(limit)+"&country="+country
    if start_date and end_date:
        base_url += "&event_date={"+str(start_date)+"|"+str(end_date)+"}&event_date_where=BETWEEN"

    response = requests.get(base_url)
    # response = requests.post(base_url)

    if response.status_code == 200:
        json_data = response.json()
        if "data" in json_data and json_data.get("success", False):
            return (json_data, pd.DataFrame(json_data["data"]))
        else:
            st.error(f"API Error: {json_data.get('message', 'Unknown error')}")
            return None
    else:
        st.error(f"HTTP Error {response.status_code}: {response.reason}")
        return None

def display_acled_data(data):
    # Convert event_date to datetime
    data[1]['event_date'] = pd.to_datetime(data[1]['event_date'])
    # Display data in a table
    st.dataframe(data[1])
    result = summary = ""

    # Download data as CSV
    csv = data[1].to_csv(index=False)
    st.download_button(
            label="Download data as CSV",
            data=csv,
            file_name='acled_data.csv',
            mime='text/csv',
        )
    if st.button("Generate Summary"):
            with st.spinner("Generating summary..."):
                json_data = data[0]
                summary = f"""
                    **Summary of the data:**
                    - **Total Records:** {len(data[1])}
                    - **Columns:** {', '.join(data[1].columns)}
                    - **Start Date:** {data[1]['event_date'].min().strftime('%Y-%m-%d')}
                    - **End Date:** {data[1]['event_date'].max().strftime('%Y-%m-%d')}
                    - **Countries:** {', '.join(data[1]['country'].unique())}
                    - **Event Types:** {', '.join(data[1]['event_type'].unique())}
                """
                model = ChatOpenAI(model="gpt-4o-mini", 
                                api_key=st.secrets["OPENAI_API_KEY"], 
                                max_tokens=1000)
                acled_prompt = """
                                    You are an ACLED expert. You have been asked to summarize 
                                    the given JSON ACLED data and give a highly detailed, informative and 
                                    structured report in markdown format, following the guidelines below.\n
                                    1. Use any headers other than the # or ## or ### headers.\n
                                    2. Do not shy away from writing too much as long as it is based on the data given.\n
                                    3. Do NOT hallucinate or make up any information.\n
                                    4. Make sure you use bullet points and tables where necessary.\n
                                    
                                    \nJSON Data: {json_data}
                                    """
                prompt = PromptTemplate.from_template(acled_prompt)
                chain = prompt | model | StrOutputParser()
                result = chain.invoke({"json_data": json_data})
                
                st.write(summary)
                st.divider()
                st.markdown(result)


if __name__ == "__main__":
    acled_page()