import wikipedia
import requests
from bs4 import BeautifulSoup
from crewai_tools import tool
import streamlit as st
import gdelt, json
import pandas as pd
from datetime import datetime, timedelta
from apify_client import ApifyClient
from modules.constants import TWEETS_COLUMNS_LIST
from apify_client.clients.resource_clients.dataset import DatasetClient
from langchain_openai import ChatOpenAI
from langchain_groq import ChatGroq
from crewai_tools import ScrapeWebsiteTool
from pages.fewsnet_map import fetch_report_content
from pages.fewsnet_map import fetch_fewsnet_reports as ffr
from huggingface_hub import hf_hub_download
import joblib

scrape_tool = ScrapeWebsiteTool()

@tool("Wikipedia Search Tool")
def search_wikipedia(query: str) -> str:
    """Run Wikipedia search and get page summaries."""
    page_titles = wikipedia.search(query)
    summaries = []

    for page_title in page_titles[:3]:  # First 3 results
        try:
            wiki_page = wikipedia.page(title=page_title, auto_suggest=False)
            summaries.append(f"Page: {page_title}\nSummary: {wiki_page.summary}")
        except wikipedia.PageError: # Page Not Found
            pass
        except wikipedia.DisambiguationError: # Disambiguation Error
            pass

    if not summaries:
        return "No good Wikipedia Search Result was found"

    return "\n\n".join(summaries)


@tool("Webpage Scraping Tool")
def scrap_webpage(target_url):
    """Scrap the content of a webpage."""
    response = requests.get(target_url)
    html_content = response.text

    soup = BeautifulSoup(html_content, "html.parser")
    stripped_content = soup.get_text()

    return stripped_content

@tool("ReliefWeb Reports Fetch Tool")
@st.cache_data(show_spinner=False)
def fetch_reliefweb_reports(number_of_reports: int = 10) -> str:
    """
    Fetches the latest ReliefWeb reports.

    Args:
        number_of_reports (int): The number of latest reports to fetch. Default is 10.

    Returns:
        str: A summarized string containing the reports' information.
    """
    url = 'https://api.reliefweb.int/v1/reports'
    params = {
        'appname': 'omdena_acaps',
        'limit': number_of_reports,
        'profile': 'full',
        'sort[]': 'date:desc'  # Sort by date descending
    }

    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        reports = data.get('data', [])
        summaries = []
        for report in reports:
            title = report['fields'].get('title', 'No Title')
            body = report['fields'].get('body', 'No Content')
            summaries.append(f"Title: {title}\nContent: {body}\n")

        # print("Fetched report: ", (number_of_reports, len(reports)))
        # print("TOOL OUTPUT\n\t\t", "\n".join(summaries))
        return f"Here are the {len(reports)} ReliwfWeb Reports fetched from their website:\n\n"+("\n".join(summaries))
    else:
        return "Failed to fetch ReliefWeb reports. Please continue with other analysis; no use wasting time here."

@tool("ReliefWeb Country-Specific Reports Fetch Tool")
@st.cache_data(show_spinner=False)
def fetch_country_specific_reliefweb_reports(country: str, num_of_reports: int = 7) -> str:
    """
    Fetches the latest ReliefWeb reports for a specific country.

    Args:
        country (str): The name of the country to fetch reports for.
        num_of_reports (int): The number of reports to fetch. Default is 7.

    Returns:
        str: A summarized string containing the reports' information.
    """
    url = 'https://api.reliefweb.int/v1/reports'
    params = {
        'appname': 'bose_acaps',
        'limit': 50,
        'profile': 'full',
        'sort[]': 'date:desc'
    }
    count = 0
    response = requests.get(url, params=params) # , timeout=10)
    if response.status_code == 200:
        data = response.json()
        reports = data.get('data', [])
        summaries = []
        for report in reports:
            title = report['fields'].get('title', 'No Title')
            body = report['fields'].get('body', 'No Content')
            if count < num_of_reports and country.lower() in body.lower():
                count += 1
                summaries.append(f"Title: {title}\nContent: {body}\n\n")

        # print("ReliefWeb Country-Specific Reports Fetch TOOL OUTPUT\n\t\t", "\n".join(summaries))
        if len(summaries) > 0:
            return f"Here are the {len(reports)} ReliwfWeb Reports fetched from their website:\n\n"+("\n".join(summaries))
        else:
            return "No country-specific reports found so no use retrying. Please carry on with other analysis."
    else:
        return "Failed to fetch ReliefWeb reports. Please carry on with other analysis."

@tool("FEWSNET Reports Fetch Tool")
@st.cache_data(show_spinner=False)
def fetch_fewsnet_reports(number_of_reports: int = 15) -> str:
    """
    Fetches the latest FEWSNET reports.

    Args:
        number_of_reports (int): The number of latest reports to fetch. Default is 15.

    Returns:
        str: A summarized string containing the reports' information.
    """
    # FEWS NET doesn't provide a public API, so we'll scrape the website
    if 'df_reports' not in st.session_state:
        st.session_state.df_reports = ffr()
    results = []
    st.session_state.df_reports = st.session_state.df_reports[:number_of_reports]
    for i in range(len(st.session_state.df_reports)):
        title = st.session_state.df_reports.iloc[i]['headline']
        report_type = st.session_state.df_reports.iloc[i]['report_type']
        description = st.session_state.df_reports.iloc[i]['description']
        content = fetch_report_content(st.session_state.df_reports.iloc[i]['article_link'])
        results.append(f"\nTitle: {title}\nReport Type: {report_type}\nDescription: {description}\n\Content: {content}\n\n")

    # print("**FEWSNET Reports Fetch Tool**\n", "\n".join(results))
    return "\n".join(results)

@tool("FEWSNET Country-Specific Reports Fetch Tool")
@st.cache_data(show_spinner=False)
def fetch_country_specific_fewsnet_reports(country: str) -> str:
    """
    Fetches the latest FEWSNET reports for a specific country.

    Args:
        country (str): The name of the country to fetch reports for.

    Returns:
        str: A summarized string containing the specified country's reports' information.
    """
    if 'df_reports' not in st.session_state:
        st.session_state.df_reports = ffr(
                # report_types=selected_report_types,
                #start_date=start_date,
                #end_date=end_date,
            )
    results, count = [], 0
    print("Fetching country-specific FEWS NET reports for:", country)
    df_country_filtered = st.session_state.df_reports[st.session_state.df_reports['place'].str.contains(country, case=False)]
    df_country_filtered = df_country_filtered[:10]
    for i in range(len(df_country_filtered)):
        title = df_country_filtered.iloc[i]['headline']
        report_type = df_country_filtered.iloc[i]['report_type']
        description = df_country_filtered.iloc[i]['description']
        content = fetch_report_content(df_country_filtered.iloc[i]['article_link'])
        if count < 15:
            results.append(f"\nTitle: {title}\nReport Type: {report_type}\nDescription: {description}\n\Cotent: {content}\n\n")
            count += 1
    
    # print("**FEWSNET Country-Specific Reports Fetch Tool**\n", "\n".join(results))

    return "\n".join(results)

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
    gd2 = gdelt.gdelt(version=2)
    if country not in country_code:
      return f"Country '{country}' not found in predefined mappings."
    if keyword not in crisis_cameo_codes:
      return f"Keyword '{keyword}' not recognized. Please provide a valid crisis type."

    try:
        results = gd2.Search([datetime.today().strftime('%Y %m %d')], table='events', coverage=False)

        # Check if results are empty
        if len(results) == 0:
            print("No results found.")
        else:
            # Convert results to a pandas DataFrame
            filtered_df = pd.DataFrame(results)

            gdelt_df = filtered_df.loc[(filtered_df.ActionGeo_CountryCode == country_code[country]) &
                                       (filtered_df.EventCode.isin(crisis_cameo_codes[keyword]))]

            return gdelt_df[['SOURCEURL', 'ActionGeo_FullName', 'CAMEOCodeDescription', 'GoldsteinScale','Actor1Name','Actor1CountryCode','Actor2Name','Actor2CountryCode','NumMentions','NumArticles']]
    except Exception as e:
        print(e)


@tool("GDELT Crisis Data Fetch Tool")
@st.cache_data(show_spinner=False)
def fetch_gdelt_data(country: str, keyword: str) -> str:
    """
    Fetches and filters GDELT crisis data based on the specified country and crisis keyword.

    Args:
        country (str): The name of the country to filter data for.
        keyword (str): The crisis type keyword (e.g., 'flood', 'earthquake', 'war') to filter events.

    Returns:
        str: A string representation of the filtered DataFrame, or a message if no data is found.
    """
    '''gdelt_df = gdelt_wrapper(country, keyword)
    if gdelt_df.empty:
        return "No data found for specified parameters."
    gdelt_df.to_csv('gdelt_data.csv', index=False)'''

    gdelt_df = pd.read_csv('C:\\Users\\user8\\OneDrive\\Documents\\Omdena-ACAPS\\ACAPS\\streamlit_app\\pages\\multiagent\\gdelt_data.csv')
    return gdelt_df.to_string(index=False)

@tool("GDELT Crisis Data URL Extractor")
@st.cache_data(show_spinner=False)
def extract_urls_from_gdelt(file_path: str = 'C:\\Users\\user8\\OneDrive\\Documents\\Omdena-ACAPS\\ACAPS\\streamlit_app\\pages\\multiagent\\gdelt_data.csv') -> list:
    """
    Extract unique URLs from the GDELT data output file.

    Args:
        file_path (str): The path to the CSV file containing GDELT data.
                         Defaults to 'C:\\Users\\user8\\OneDrive\\Documents\\Omdena-ACAPS\\ACAPS\\streamlit_app\\pages\\multiagent\\gdelt_data.csv'.

    Returns:
        list: A list of unique URLs extracted from the 'SOURCEURL' column
              in the GDELT data file. Returns an empty list if the column
              does not exist or the file is empty.
    """
    try:
        # Read the CSV file directly
        df = pd.read_csv(file_path)
        if 'SOURCEURL' in df.columns:
            return df['SOURCEURL'].unique().tolist()  # Return unique URLs
        return []  # Return an empty list if the column is missing
    except Exception as e:
        return f"Error in extracting URLs: {e}"

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

@tool("Twitter Data Fetch Tool")
@st.cache_data(show_spinner=False)
def fetch_twitter_data(keyword: str, country: str):
    """
    Fetches top 20 tweets based on the specified country and crisis keyword.

    Args:
        keyword (str): The crisis type keyword (e.g., 'flood', 'earthquake') to filter events.
        country (str): The name of the country to filter data for.

    Returns:
        str: A string representation of the filtered DataFrame, or a message if no data is found.
    """
    # print(f"Fetching tweets for keyword: {keyword}, country: {country}")
    client= ApifyClient(token=st.secrets["APIFY_TOKEN"])
    
    # Update the input parameters as per your specified query
    run_input = {
        "maxItems": 20,
        "includeSearchTerms": False,
        "onlyImage": False,
        "onlyQuote": False,
        "onlyTwitterBlue": False,
        "onlyVerifiedUsers": False,
        "onlyVideo": False,
        #"geotaggedNear":f"{country}",
        "searchTerms": [
            #f"({keyword})"
            f"({keyword}) ({country})"
        ],
        "sort": "Top",
    }

    try:
        df = pd.read_csv('C:\\Users\\user8\\OneDrive\\Documents\\Omdena-ACAPS\\ACAPS\\streamlit_app\\pages\\multiagent\\twitter_data.csv')
        # print(df.sample(10))
        return df.to_string(index=False)

    except Exception as e:
        # print(f"Error fetching Twitter data: {e}")
        return pd.DataFrame(columns=TWEETS_COLUMNS_LIST)

@tool("Twitter Data URL Extractor")
@st.cache_data(show_spinner=False)
def extract_text_from_twitter(file_path: str = 'C:\\Users\\user8\\OneDrive\\Documents\\Omdena-ACAPS\\ACAPS\\streamlit_app\\pages\\multiagent\\twitter_data.csv') -> list:
    """
    Extract text from the twitter data output file.

    Args:
        file_path (str): The path to the CSV file containing twitter data.
                         Defaults to 'C:\\Users\\user8\\OneDrive\\Documents\\Omdena-ACAPS\\ACAPS\\streamlit_app\\pages\\multiagent\\twitter_data.csv'.

    Returns:
        list: A list of text extracted from the 'text' column
              in the twitter data file. Returns an empty list if the column
              does not exist or the file is empty.
    """
    try:
        # Read the CSV file directly
        df = pd.read_csv(file_path)
        if 'text' in df.columns:
            return df['text'].unique().tolist()
        return []
    except Exception as e:
        return f"Error in extracting text: {e}"
    
@tool("Google Trending Searches Fetch Tool")
@st.cache_data(show_spinner=False)
def google_trending_searches(country: str) -> list:
    """
    Fetches trending searches from Google Trends for a given country and return a list.

    Args:
        country (str): The name of the country.

    Returns:
        list: A list of trending searches with metadata.
    """
    client = ApifyClient(token=st.secrets["APIFY_TOKEN"])
    country_codes = {
        "Argentina": "AR", "Australia": "AU", "Austria": "AT", "Belgium": "BE",
        "Brazil": "BR", "Canada": "CA", "Chile": "CL", "Colombia": "CO",
        "Czech Republic": "CZ", "Denmark": "DK", "Egypt": "EG", "Finland": "FI",
        "France": "FR", "Germany": "DE", "Greece": "GR", "Hong Kong": "HK",
        "Hungary": "HU", "India": "IN", "Indonesia": "ID", "Ireland": "IE",
        "Israel": "IL", "Italy": "IT", "Japan": "JP", "Kenya": "KE",
        "Malaysia": "MY", "Mexico": "MX", "Netherlands": "NL", "New Zealand": "NZ",
        "Nigeria": "NG", "Norway": "NO", "Philippines": "PH", "Poland": "PL",
        "Portugal": "PT", "Romania": "RO", "Russia": "RU", "Saudi Arabia": "SA",
        "Singapore": "SG", "South Africa": "ZA", "South Korea": "KR", "Sweden": "SE",
        "Switzerland": "CH", "Taiwan": "TW", "Thailand": "TH", "Turkey": "TR",
        "Ukraine": "UA", "United Kingdom": "GB", "United States": "US", "Vietnam": "VN"
    }
    if country not in country_codes:
        return [f"Selection of {country} is not available."]

    run_input = {
        "geo": country_codes[country],
        "outputMode": "complete",
        "fromDate": "today",
        "toDate": "3 days",
        "maxItems": 100,
        "proxy": {"useApifyProxy": True},
        "extendOutputFunction": "async ({ data, item }) => item",
    }

    try:
        run = client.actor("49HfNLFgg6B8YetTj").call(run_input=run_input)
        dataset_id = run.get("defaultDatasetId", "")
        dataset: DatasetClient = client.dataset(dataset_id)
        records = list(dataset.iterate_items())
        return records
    except Exception as e:
        return [f"Error fetching data: {e}"]

def find_query_data(dataset, query):
    for entry in dataset:
        if entry['query'] == query:
            return entry
    return None

@tool("Google Trending Searches Filter Tool")
@st.cache_data(show_spinner=False)
def filter_trends_query(records: list) -> str:
    """
    Filters a list of trending search queries for crisis relevance using a Llama3 model.
    Returns a string representation of a DataFrame containing relevant queries along with their descriptions and URLs.

    Args:
        records (list): A list of dictionaries where each dictionary contains information about a trending topic.
        Each entry in the list should have the following structure:

            [
                {
                    "query": str,               # The main search query (e.g., "Sporting vs Arsenal").
                    "exploreLink": str,         # URL for exploring the query on Google Trends.
                    "geo": str,                 # Geographic location code (e.g., "KE" for Kenya).
                    "date": str,                # Date of the trending search in ISO format (e.g., "2024-11-26T00:00:00.000Z").
                    "formattedTraffic": int,    # Traffic volume indicator for the query.
                    "relatedQueries": [         # A list of related queries.
                        {
                            "query": str,       # A related query.
                            "exploreLink": str  # URL for exploring the related query.
                        },
                        ...
                    ],
                    "articles": [               # A list of related news articles.
                        {
                            "title": str,       # Article title.
                            "timeAgo": str,     # Time since publication (e.g., "16h ago").
                            "source": str,      # Source of the article (e.g., "Sky Sports").
                            "url": str,         # URL of the article.
                            "snippet": str,     # Brief snippet of the article content.
                            "image": {          # Information about the article's image.
                                "newsUrl": str,  # URL of the article with the image.
                                "source": str,   # Image source.
                                "imageUrl": str  # URL of the image.
                            }
                        },
                        ...
                    ]
                },
                ...
            ]

    Returns:
        str: A string representation of a DataFrame containing filtered queries. Each row includes:
            - query: The query string.
            - description: A brief explanation of why it's relevant.
            - urls: Associated URLs for further information.

        The DataFrame is also saved as a CSV file named 'gtrends.csv'.

    Raises:
        ValueError: If the input 'records' is not a list or contains malformed entries.
        Exception: For other unexpected errors during filtering.

    Example:
        >>> records = [
                {
                    "query": "Sporting vs Arsenal",
                    "exploreLink": "https://trends.google.com/trends/explore?q=Sporting+vs+Arsenal&date=now+7-d&geo=KE",
                    "geo": "KE",
                    "date": "2024-11-26T00:00:00.000Z",
                    "formattedTraffic": 100000,
                    "relatedQueries": [
                        {"query": "Arsenal", "exploreLink": "https://trends.google.com/trends/explore?q=Arsenal&date=now+7-d&geo=KE"}
                    ],
                    "articles": [
                        {
                            "title": "Sporting 1-5 Arsenal: Match Highlights",
                            "timeAgo": "16h ago",
                            "source": "Sky Sports",
                            "url": "https://www.skysports.com/football/sporting-vs-arsenal/report/521678",
                            "snippet": "Match report as Arsenal dominate Sporting...",
                            "image": {
                                "newsUrl": "https://www.skysports.com/football/sporting-vs-arsenal/report/521678",
                                "source": "Sky Sports",
                                "imageUrl": "https://t3.gstatic.com/images?q=tbn:ANd9GcSt..."
                            }
                        }
                    ]
                }
            ]

        >>> filter_trends_query(records)
        "query        description                         urls\n
            Sporting vs Arsenal  Match Highlights   ['https://www.skysports.com/...', 'https://www.football.london/...']"
    """

    query_list = set([val['query'] for val in records])

    try:
        model = ChatOpenAI(api_key=st.secrets["OPENAI_API_KEY"],
                           model="gpt-4o-mini",
                           response_format={"type": "json_object"})

        messages = [("system", "You are a helpful assistant, who is expert researcher, who knows several languages. "
                                "You filter the lists of queries according to the criteria"), ("human", f""" From the
                                following list of {query_list}, filter and return the list of terms which are important
                                indicator of crisis as 'query':'description' in json format,
                                e.g. if trending search queries are related to a sports event such as match or name of the sporting team, don't include it unless it accompanied by another crisis even, such as riot or brawl during the match """)
                    ]

        response = model.invoke(messages)
        filtered_searches = json.loads(response.content)
        description_key = list(filtered_searches.keys())[0]
        queries_df = pd.DataFrame(filtered_searches[description_key])
        filtered_queries = [k['query'] for k in filtered_searches[description_key]]

        knowledge_base = {}
        for i, target_query in enumerate(filtered_queries):
            result = find_query_data(records, target_query)
            # print(f"\nQuery: {target_query}")
            knowledge_base[target_query] = [r['url'] for r in result['articles']][:5]

        # Display the updated DataFrame
        #return df_gtrends.to_string(index=False)
                # Add URLs to DataFrame
        queries_df['urls'] = queries_df['query'].map(knowledge_base)
        queries_df.to_csv('gtrends.csv', index=False)  # Save to CSV
        return queries_df.to_string(index=False)
    except Exception as e:
        return(f"error {e}")

@tool("ACLED Data Fetch Tool")
@st.cache_data(show_spinner=False)
def fetch_acled_data(country:str, event_types:str, start_date:str, end_date:str, limit: int = 250) -> str: 
    """
    Fetches ACLED data based on the specified parameters.

    Args:
        country (str): The name of the country to filter data for. If you are fetching data for all countries, set this to "All".
        event_types (str): The type of event to filter data for.
        start_date (str): The start date for filtering data. Format is "YYYY-MM-DD".
        end_date (str): The end date for filtering data. Format is "YYYY-MM-DD".
        limit (int): The maximum number of records to fetch.

    Returns:
        tuple: A string containing the JSON response from the API, or None if the request fails.
    
    """
    if country == "All":
        base_url = "https://api.acleddata.com/acled/read/?key="+st.secrets["ACLED_API_KEY"]+"&email="+st.secrets["ACLED_EMAIL"]+"&limit="+str(limit)
    else:
        base_url = "https://api.acleddata.com/acled/read/?key="+st.secrets["ACLED_API_KEY"]+"&email="+st.secrets["ACLED_EMAIL"]+"&limit="+str(limit)+"&country="+country
    if start_date and end_date:
        base_url += "&event_date={"+str(start_date)+"|"+str(end_date)+"}&event_date_where=BETWEEN"

    response = requests.get(base_url)
    # response = requests.post(base_url)

    if response.status_code == 200:
        json_data = response.json()
        if "data" in json_data and json_data.get("success", False):
            return str(json_data)
        else:
            st.error(f"API Error: {json_data.get('message', 'Unknown error')}")
            return None
    else:
        st.error(f"HTTP Error {response.status_code}: {response.reason}")
        return None

'''@tool("INFORM Severity Prediction Tool")
@st.cache_data(show_spinner=False)
def inform_severity_prediction(country: str) -> float:
    """
    Predicts the INFORM Severity Index of a crisis for the following given parameters.

    Args:
        country (str): The name of the country.

    Returns:
        float: Predicted INFORM Severity Index of the given crisis.
    """
    # Load the pre-trained model and preprocessor
    transformer = joblib.load(hf_hub_download("ChukwudiAsibe/ACAP_Severity_Inform_Index", "preprocessor.joblib"))
    transformed_data = transformer.transform(Test.drop(['Inform Severity Index', 'Crisis Id'], axis=1))
    transformed_test = pd.DataFrame(transformed_data)
    transformed_test.columns = transformer.get_feature_names_out()
    transformed_test.index = Test.index
    model = joblib.load(hf_hub_download("ChukwudiAsibe/ACAP_Severity_Inform_Index", "model.joblib"))

    predicted_SII = pd.DataFrame(model.predict(transformed_test)).round(2)
    predicted_SII.columns = ['Predicted_Inform_Severity_Index']
    predicted_SII.index = Test.index
    return float(predicted_SII)'''