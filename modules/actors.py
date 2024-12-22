import re
import pandas as pd
import streamlit as st
from datetime import datetime
from typing import Dict, List, Any
from apify_client import ApifyClient
from apify_client.clients.resource_clients.dataset import DatasetClient
from langchain_groq import ChatGroq
import requests  # For GDELT API requests
import time
import numpy as np
import json
import pdb
import gdelt

# Initialize GDELT 2.0
gd2 = gdelt.gdelt(version=2)  #for GDELT data

# Constants for Apify Actors
APIFY_TWITTER_ACTOR_ID = '61RPP7dywgiy0JPD0'  # Replace with actual Twitter scraper actor ID
APIFY_GOOGLE_TRENDS_ACTOR_ID = '49HfNLFgg6B8YetTj'  # Google Trending Searches actor ID

# Columns to keep from the scraped data
TWEETS_COLUMNS_LIST = [
    "id",
    "url",
    "text",
    "createdAt",
    "retweetCount",
    "replyCount",
    "likeCount",
    "quoteCount",
    "bookmarkCount",
    "author_name",
    "author_followers",
    "author_isVerified",
    "author_userName",
    "author_profilePicture",
    "author_location",
    "author_createdAt",
    "author_statusesCount",
    "author_following",
    "author_favouritesCount",
    "author_isBlueVerified"
]

# Apify API Token
#APIFY_TOKEN = st.secrets["APIFY_TOKEN"]

# Initialize the Apify client
#client = ApifyClient(APIFY_TOKEN)

# Country coordinates mapping for geotargeting (latitude, longitude, radius)
COUNTRY_COORDINATES = {
    "Sudan": "15.5007,32.5599,500km",  # Sudan with a 500km radius
    "United States": "37.0902,-95.7129,1000km",
    "India": "20.5937,78.9629,1000km",
    "Mali": "17.5707,-3.9962,500km",
    "Myanmar": "21.9162,95.9560,500km",
    "Burkina Faso": "12.2383,-1.5616,500km"
}


# Function to clean text
@st.cache_data
def clean_text(text):
    text = text.lower()
    text = re.sub(r'https?://\S+|www\.\S+', '', text)  # Remove URLs
    text = re.sub(r'@\w+', '', text)  # Remove mentions
    text = re.sub(r'#\w+', '', text)  # Remove hashtags and the words following them
    text = re.sub(r'[^\w\s]', '', text)  # Remove punctuation
    text = re.sub(r'\s+', ' ', text).strip()  # Remove extra whitespace
    text = re.sub(r'[\U00010000-\U0010FFFF]', '', text)  # Remove emojis
    return text if text else None  # Return None if the text is empty


# Flatten the response
@st.cache_data
def flatten_response(response):
    author_info = response.get("author", {})
    return {
        "id": response.get("id"),
        "url": response.get("url"),
        "text": response.get("text"),
        "createdAt": pd.to_datetime(response.get("createdAt")),
        "retweetCount": response.get("retweetCount"),
        "replyCount": response.get("replyCount"),
        "likeCount": response.get("likeCount"),
        "quoteCount": response.get("quoteCount"),
        "bookmarkCount": response.get("bookmarkCount"),
        "author_name": author_info.get("name"),
        "author_followers": author_info.get("followers"),
        "author_isVerified": author_info.get("isVerified"),
        "author_userName": author_info.get("userName"),
        "author_profilePicture": author_info.get("profilePicture"),
        "author_location": author_info.get("location"),
        "author_createdAt": pd.to_datetime(author_info.get("createdAt")),
        "author_statusesCount": author_info.get("statusesCount"),
        "author_following": author_info.get("following"),
        "author_favouritesCount": author_info.get("favouritesCount"),
        "author_isBlueVerified": author_info.get("isBlueVerified")
    }



# Function to fetch Twitter data using Apify
@st.cache_data
def fetch_twitter_data(keyword, country, start_date=None, end_date=None ):
    #pdb.set_trace()
    client= ApifyClient(st.secrets['APIFY_TWITTER_TOKEN'])
    # Prepare run input with geocode if country is found in the mapping
    geocode = COUNTRY_COORDINATES.get(country, None)

    # Update the input parameters as per your specified query
    run_input = {
        "maxItems": 50,
        "includeSearchTerms": False,
        "onlyImage": False,
        "onlyQuote": False,
        "onlyTwitterBlue": False,
        "onlyVerifiedUsers": False,
        "onlyVideo": False,
        "searchTerms": [
            f"({keyword}) ({country})"
        ],
        "sort": "Top",
        "start": start_date.strftime('%Y-%m-%d') if start_date else None,  # Add start date
        "end": end_date.strftime('%Y-%m-%d') if end_date else None,       # Add end date
    }

    # Add geolocation data if available
    #if geocode:
    #run_input["geocode"] = geocode

    try:
        run = client.actor(APIFY_TWITTER_ACTOR_ID).call(run_input=run_input)

        # Log the run result to check for issues
        print("Twitter Run Response:", run)

        # Fetch the results from the dataset
        response = [
            dictionary
            for dictionary in client.dataset(run["defaultDatasetId"]).iterate_items()
        ]

        if not response:  # Check if the response is empty
            print("Twitter response is empty.")

        flattened_data = [flatten_response(tweet) for tweet in response]
        df = pd.DataFrame(flattened_data, columns=TWEETS_COLUMNS_LIST)
        #df['cleaned_text'] = df['text'].apply(clean_text)


        # Display the updated DataFrame
        return df

    except Exception as e:
        print(f"Error fetching Twitter data: {e}")
        return pd.DataFrame(columns=TWEETS_COLUMNS_LIST)  # Return an empty DataFrame in case of error
    

# Function to run the twitter scraper
@st.cache_data
def run_apify_twitter_actor(selected_country, selected_keyword, start_date=None, end_date=None):

    
    if "top_tweets" in st.session_state:
        top_tweets = st.session_state["top_tweets"]


    # Fetch Twitter data
    twitter_data = fetch_twitter_data(selected_keyword, selected_country, start_date, end_date)

    # Check if twitter_data is None, and set it to an empty DataFrame if so
    if twitter_data is None or twitter_data.empty:
        print("Warning: twitter_data is empty, returning empty DataFrame")
        twitter_data = pd.DataFrame(columns=TWEETS_COLUMNS_LIST)
        st.warning("No tweets found for the selected criteria.")
        return twitter_data  # Return immediately if no data is available

    return twitter_data

# Function to run all the scrapers
@st.cache_data
def run_apify_actors(selected_country, selected_keyword):

    google_trends_data = google_trending_searches(selected_country)
    gdelt_news_data = gdelt_wrapper(selected_country, selected_keyword)

    return google_trends_data, gdelt_news_data


@st.cache_data
def google_trending_searches(country):
    client = ApifyClient(token=st.secrets['APIFY_TOKEN'])
    country_codes = {
        "Argentina": "AR",
        "Australia": "AU",
        "Austria": "AT",
        "Belgium": "BE",
        "Brazil": "BR",
        "Canada": "CA",
        "Chile": "CL",
        "Colombia": "CO",
        "Czech Republic": "CZ",
        "Denmark": "DK",
        "Egypt": "EG",
        "Finland": "FI",
        "France": "FR",
        "Germany": "DE",
        "Greece": "GR",
        "Hong Kong": "HK",
        "Hungary": "HU",
        "India": "IN",
        "Indonesia": "ID",
        "Ireland": "IE",
        "Israel": "IL",
        "Italy": "IT",
        "Japan": "JP",
        "Kenya": "KE",
        "Malaysia": "MY",
        "Mexico": "MX",
        "Netherlands": "NL",
        "New Zealand": "NZ",
        "Nigeria": "NG",
        "Norway": "NO",
        "Philippines": "PH",
        "Poland": "PL",
        "Portugal": "PT",
        "Romania": "RO",
        "Russia": "RU",
        "Saudi Arabia": "SA",
        "Singapore": "SG",
        "South Africa": "ZA",
        "South Korea": "KR",
        "Sweden": "SE",
        "Switzerland": "CH",
        "Taiwan": "TW",
        "Thailand": "TH",
        "Turkey": "TR",
        "Ukraine": "UA",
        "United Kingdom": "GB",
        "United States": "US",
        "Vietnam": "VN"
    }

    try:
        if country not in country_codes.keys():
            st.warning(f"Selection of {country} is not available via Apify Google Trends Search Actor")

        else:

            # Prepare the Actor input
            run_input = {
                "geo": country_codes[country],
                "outputMode": "complete",
                "fromDate": "today",
                "toDate": "3 days",
                "maxItems": 100,
                "proxy": {"useApifyProxy": True},
                "extendOutputFunction": """async ({ data, item, request, customData, fromDate, toDate, Apify }) => {
              return item;
            }""",
                "extendScraperFunction": """async ({ data, item, request, addUrl, customData, fromDate, toDate, extendOutputFunction, Apify }) => {
    
            }""",
                "customData": {},
            }

            # Run the Actor and wait for it to finish

            run: dict | None = client.actor("49HfNLFgg6B8YetTj").call(run_input=run_input)

            dataset_id: str = run.get("defaultDatasetId", "")

            # Retrieve dataset
            dataset: DatasetClient = client.dataset(dataset_id)

            # Retrieve records from the dataset
            records: List[Dict[str, Any]] = list(dataset.iterate_items())

            return records

    except Exception as e:
        return f"error {e}"


@st.cache_data
def llama_filter_chatgroq(query_list: str):
    try:
        groq = ChatGroq(api_key=st.secrets['GROQ_API_KEY'],
                        temperature=0,
                        model_name="llama-3.1-70b-versatile",
                        response_format={"type": "json_object"})

        messages = [("system", "You are a helpful assistant, who is expert researcher, who knows several languages. "
                               "You filter the lists of queries according to the criteria"), ("human", f""" From the 
                               following list of {query_list}, filter and return the list of terms which are important 
                               indicator of crisis as 'query':'description' in json format """)
                    ]

        response = groq.invoke(messages)
        return json.loads(response.content)
    except Exception as e:
        st.error(f"error {e}")


@st.cache_data
def google_trends_for_url(url: str):
    try:
        client = ApifyClient(token=st.secrets['APIFY_TOKEN'])
        # Prepare the Actor input
        run_input = {
            "isMultiple": False,
            "isPublic": False,
            "searchTerms": [],
            "skipDebugScreen": False,
            "startUrls": [
                {
                    "url": url,
                    "method": "GET"
                }
            ],
            "timeRange": "",
            "geo": "",
            "category": "",
            "maxItems": 0,
            "maxConcurrency": 10,
            "maxRequestRetries": 7,
            "pageLoadTimeoutSecs": 60
        }
        # Run the Actor and wait for it to finish
        run = client.actor("DyNQEYDj9awfGQf9A").call(run_input=run_input)

        dataset_id = run.get("defaultDatasetId", "")

        # Retrieve dataset
        dataset = client.dataset(dataset_id)

        # Retrieve records from the dataset
        records = list(dataset.iterate_items())
        return records
    except Exception as e:
        st.error(f"error {e}")


@st.cache_data
def gdelt_wrapper(country, keyword):
    crisis_cameo_codes = {
        "earthquake": ["0233"],  # Appeal for humanitarian aid
        "flood": ["0233", "0234"],  # Appeal for humanitarian aid, Appeal for military protection or peacekeeping
        "famine": ["0233"],  # Appeal for humanitarian aid
        "drought": ["0233"],  # Appeal for humanitarian aid
        "wildfire": ["0233"],  # Appeal for humanitarian aid
        "tornado": ["0233"],  # Appeal for humanitarian aid
        "hurricane": ["0233", "0234"],  # Appeal for humanitarian aid, Appeal for military protection
        "tsunami": ["0233"],  # Appeal for humanitarian aid
        "landslide": ["0233"],  # Appeal for humanitarian aid
        "volcanic eruption": ["0233"],  # Appeal for humanitarian aid
        "economic crisis": ["0231", "1031"],  # Appeal and Demand for economic aid
        "financial crisis": ["0231", "1031"],  # Appeal and Demand for economic aid
        "health crisis": ["0233"],  # Appeal for humanitarian aid
        "pandemic": ["0233", "0234"],  # Appeal for humanitarian aid, Appeal for military protection
        "epidemic": ["0233"],  # Appeal for humanitarian aid
        "civil unrest": ["145", "172"],  # Protest violently, Impose administrative sanctions
        "protests": ["143", "144"],  # Conduct strike or boycott, Obstruct passage
        "riots": ["145"],  # Protest violently
        "military conflict": ["190", "193", "195"],
        # Use conventional military force, Fight with small arms, Employ aerial weapons
        "war": ["190", "195", "200"],
        # Use conventional military force, Employ aerial weapons, Use unconventional mass violence
        "terrorist attack": ["1383", "180"],  # Threaten unconventional attack, Use unconventional violence
        "cyber attack": ["176"],  # Attack cybernetically
        "hostage situation": ["181"],  # Abduct, hijack, take hostage
        "kidnapping": ["181"],  # Abduct, hijack, take hostage
        "blockade": ["191"],  # Impose blockade
        "embargo": ["163"],  # Impose embargo, boycott, or sanctions
        "political instability": ["120", "130"],  # Reject, Threaten
        "martial law": ["1724"],  # Impose state of emergency or martial law
        "state of emergency": ["1724"],  # Impose state of emergency or martial law
        "environmental disaster": ["0233"],  # Appeal for humanitarian aid
        "chemical spill": ["2041"],  # Use chemical weapons
        "nuclear incident": ["2042"],  # Detonate nuclear weapons
        "biological threat": ["2041"],  # Use biological weapons
        "violent repression": ["175"],  # Use tactics of violent repression
        "ethnic cleansing": ["203"]  # Engage in ethnic cleansing
    }
    country_code = {
        'Afghanistan': 'AF',
        'Albania': 'AL',
        'Algeria': 'AG',
        'Antarctica': 'AY',
        'Antigua And Barbuda': 'AC',
        'Argentina': 'AR',
        'Australia': 'AS',
        'Austria': 'AU',
        'Azerbaijan': 'AJ',
        'Bahamas': 'BF',
        'Bahrain': 'BA',
        'Bangladesh': 'BG',
        'Barbados': 'BB',
        'Belize': 'BH',
        'Belgium': 'BE',
        'Benin': 'BN',
        'Bermuda': 'BD',
        'Bhutan': 'BT',
        'Bolivia': 'BL',
        'Bosnia-Herzegovina': 'BK',
        'Botswana': 'BW',
        'Brazil': 'BR',
        'Brunei': 'BX',
        'Bulgaria': 'BU',
        'Burundi': 'BY',
        'Cambodia': 'CB',
        'Cameroon': 'CM',
        'Canada': 'CA',
        'Chad': 'CD',
        'Chile': 'CI',
        'China': 'CH',
        'Colombia': 'CO',
        'Congo': 'CF',
        'Cook Islands': 'CW',
        'Cuba': 'CU',
        'Cyprus': 'CY',
        'Denmark': 'DA',
        'Djibouti': 'DJ',
        'Dominican Republic': 'DR',
        'Ecuador': 'EC',
        'Egypt': 'EG',
        'El Salvador': 'ES',
        'Eritrea': 'ER',
        'Estonia': 'EN',
        'Ethiopia': 'ET',
        'Finland': 'FI',
        'France': 'FR',
        'Gambia': 'GA',
        'Gaza Strip': 'GZ',
        'Germany': 'GM',
        'Ghana': 'GH',
        'Gibraltar': 'GI',
        'Greece': 'GR',
        'Grenada': 'GJ',
        'Guam': 'GQ',
        'Guatemala': 'GT',
        'Guinea': 'GV',
        'Guyana': 'GY',
        'Haiti': 'HA',
        'Honduras': 'HO',
        'Hong Kong': 'HK',
        'Hungary': 'HU',
        'India': 'IN',
        'Indonesia': 'ID',
        'Iran': 'IR',
        'Iraq': 'IZ',
        'Ireland': 'EI',
        'Israel': 'IS',
        'Italy': 'IT',
        'Jamaica': 'JM',
        'Japan': 'JA',
        'Jersey': 'JE',
        'Jordan': 'JO',
        'Kazakhstan': 'KZ',
        'Kenya': 'KE',
        'Kyrgyzstan': 'KG',
        'Laos': 'LA',
        'Latvia': 'LG',
        'Lebanon': 'LE',
        'Libya': 'LY',
        'Malawi': 'MI',
        'Malaysia': 'MY',
        'Maldives': 'MV',
        'Mali': 'ML',
        'Malta': 'MT',
        'Mauritania': 'MR',
        'Mexico': 'MX',
        'Moldova': 'MD',
        'Mongolia': 'MG',
        'Montenegro': 'MJ',
        'Morocco': 'MO',
        'Namibia': 'WA',
        'Nepal': 'NP',
        'Netherlands': 'NL',
        'New Zealand': 'NZ',
        'Nicaragua': 'NU',
        'Nigeria': 'NI',
        'Niue': 'NE',
        'North Korea': 'KN',
        'Norway': 'NO',
        'Pakistan': 'PK',
        'Palau': 'PS',
        'Panama': 'PM',
        'Papua New Guinea': 'PP',
        'Peru': 'PE',
        'Philippines': 'RP',
        'Poland': 'PL',
        'Portugal': 'PO',
        'Qatar': 'QA',
        'Rwanda': 'RW',
        'Saudi Arabia': 'SA',
        'Serbia': 'RI',
        'Singapore': 'SN',
        'South Africa': 'SF',
        'South Korea': 'KS',
        'South Sudan': 'OD',
        'Spain': 'SP',
        'Sri Lanka': 'CE',
        'Sudan': 'SU',
        'Sweden': 'SW',
        'Switzerland': 'SZ',
        'Syria': 'SY',
        'Taiwan': 'TW',
        'Tanzania': 'TZ',
        'Thailand': 'TH',
        'Tonga': 'TN',
        'Turkey': 'TU',
        'Turkmenistan': 'TX',
        'Uganda': 'UG',
        'Ukraine': 'UP',
        'United Arab Emirates': 'AE',
        'United Kingdom': 'UK',
        'United States': 'US',
        'Uzbekistan': 'UZ',
        'Venezuela': 'VE',
        'Vietnam': 'VM',
        'West Bank': 'WE',
        'Yemen': 'YM',
        'Zambia': 'ZA',
        'Zimbabwe': 'ZI'
    }

    try:
        # Query GDELT data
        results = gd2.Search([datetime.today().strftime('%Y %m %d')], table='events', coverage=False)

        if len(results) == 0:
            st.write("No results found.")
            return pd.DataFrame()

        filtered_df = pd.DataFrame(results)

        # Validate the keyword and country inputs
        if keyword not in crisis_cameo_codes:
            st.error(f"Keyword '{keyword}' not found in CAMEO mappings.")
            return pd.DataFrame()

        if country not in country_code:
            st.error(f"Country '{country}' not recognized.")
            return pd.DataFrame()

        # Check if the EventCode exists in the data
        matching_event_codes = filtered_df['EventCode'].isin(crisis_cameo_codes[keyword]).any()

        if matching_event_codes:
            # Filter by both country and event codes
            gdelt_df = filtered_df.loc[
                (filtered_df.ActionGeo_CountryCode == country_code[country]) &
                (filtered_df.EventCode.isin(crisis_cameo_codes[keyword]))
                ]

            if gdelt_df.shape[0] == 0:
                gdelt_df = filtered_df.loc[
                    (filtered_df.ActionGeo_CountryCode == country_code[country])
                ]
        else:
            # Filter only by country if no matching event codes
            gdelt_df = filtered_df.loc[
                (filtered_df.ActionGeo_CountryCode == country_code[country])
            ]

        # Return relevant columns
        gdelt_df[[
            'SOURCEURL', 'ActionGeo_FullName', 'CAMEOCodeDescription', 'GoldsteinScale',
            'Actor1Name', 'Actor1CountryCode', 'Actor2Name', 'Actor2CountryCode', 'NumMentions', 'NumArticles'
        ]].to_csv('gdelt.csv')
        return gdelt_df[[
            'SOURCEURL', 'ActionGeo_FullName', 'CAMEOCodeDescription', 'GoldsteinScale',
            'Actor1Name', 'Actor1CountryCode', 'Actor2Name', 'Actor2CountryCode', 'NumMentions', 'NumArticles'
        ]]
    except Exception as e:
        st.error(f"An error occurred: {e}")
        return pd.DataFrame()

