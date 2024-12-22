import streamlit as st
import folium
from streamlit_folium import st_folium
import pandas as pd
from tqdm import tqdm
import requests
from bs4 import BeautifulSoup
from dateutil import parser
from modules.constants import COUNTRIES
from concurrent.futures import ThreadPoolExecutor, as_completed
import json
import os
from datetime import datetime
from urllib.parse import urlencode
import geopandas as gpd
from shapely.geometry import Point

# Constants
REPORT_TYPE_MAPPING = {
    "Alert": "17",
    "Targeted Analysis": "39",
    "Special Report": "8"
}

TOPIC_MAPPING = {
    "Integrated Food Security Analysis": "41",
    "Agroclimatology": "42",
    "Markets & Trade": "43",
    "Nutrition": "44"
}

BASE_URL = "https://fews.net/search"
HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

def load_geojson():
    geojson_path = os.path.join(os.path.dirname(__file__), 'countries.geojson')
    with open(geojson_path, 'r') as f:
        geojson_data = json.load(f)
    return geojson_data

def date_to_timestamp(date_str):
    """Convert a date string to a Unix timestamp, accepting multiple formats."""
    for date_format in ["%m/%d/%Y", "%Y-%m-%d"]:
        try:
            dt = datetime.strptime(str(date_str), date_format)
            return int(dt.timestamp())
        except ValueError:
            continue
    raise ValueError(f"Date '{date_str}' does not match any supported format ('mm/dd/yyyy' or 'dd-mm-yyyy').")

def validate_date_range(end_date):
    """Ensure the end_date is not greater than today's date."""
    if end_date:
        today = datetime.now()
        end_date_obj = datetime.strptime(str(end_date), "%Y-%m-%d")
        if end_date_obj > today:
            st.error(f"End date {end_date} cannot be later than today's date ({today.strftime('%Y-%m-%d')}).")
            # raise ValueError(f"End date {end_date} cannot be later than today's date ({today.strftime('%m/%d/%Y')}).")

def convert_to_ids(values, mapping):
    """Converts a list of text values to their corresponding numeric IDs."""
    if not values:
        return None
    converted = []
    for value in values:
        # If the value is already numeric, keep it
        if str(value).isdigit():
            converted.append(value)
        # Convert text to its corresponding numeric ID
        elif value in mapping:
            converted.append(mapping[value])
        else:
            raise ValueError(f"Invalid value '{value}'. Must be one of {list(mapping.keys())}.")
    return converted

def get_next_page_url(soup):
    """Gets the next page URL from the current soup object."""
    next_page_tag = soup.find('a', title='Go to next page')
    if next_page_tag and next_page_tag.get('href'):
        return f"https://fews.net/search{next_page_tag.get('href')}"
    return None

def get_report_count(fewsnet_url):
    """Fetch the total number of reports for the given URL."""
    response = requests.get(fewsnet_url, headers=HEADERS)
    soup = BeautifulSoup(response.text, "html.parser")
    count_tag = soup.find('fews-facet-links-item')
    if count_tag and count_tag.get('count'):
        return int(count_tag.get('count'))
    return 0

def get_page_content(url):
    """Fetch page content from the URL."""
    response = requests.get(url, headers=HEADERS)
    response.raise_for_status()
    return BeautifulSoup(response.text, "html.parser")

def fetch_report_content(report_url=None):
    """Fetches the content of a specified FEWSNET report URL."""
    if not report_url:
        raise ValueError("Report URL must be provided.")

    soup = get_page_content(report_url)
    content_sections = soup.find_all('div', class_='report-section')

    # Use list comprehension and join for more efficient string concatenation
    content = ' '.join([section.get_text(strip=True) for section in content_sections])

    return content

def scrape_fewsnet(report_types, start_date, end_date, topics, keywords, report_count):
    """Main function to scrape FEWS NET with filters, multithreading, and progress tracking."""
    base_url = build_url(report_types, start_date, end_date, topics, keywords)
    all_data = []
    urls_to_scrape = [base_url]

    # Crawl through pages to gather URLs to scrape
    while len(all_data) < report_count:
        soup = get_page_content(urls_to_scrape[-1])
        all_data.extend(extract_page_data(soup))
        next_page_url = get_next_page_url(soup)
        if next_page_url:
            urls_to_scrape.append(next_page_url)
        else:
            break
    # Initialize progress bar
    pbar = tqdm(total=report_count, desc="Scraping reports", unit="report")
    # Use multithreading to scrape each page
    data = []
    with ThreadPoolExecutor(max_workers=5) as executor:
        future_to_url = {executor.submit(get_page_content, url): url for url in urls_to_scrape}
        for future in as_completed(future_to_url):
            url = future_to_url[future]
            try:
                soup = future.result()
                page_data = extract_page_data(soup)
                data.extend(page_data)
                
                # Update progress bar by the number of reports added
                pbar.update(len(page_data))
            except Exception as e:
                print(f"Error fetching data from {url}: {e}")
    # Close the progress bar
    pbar.close()
    # Convert to DataFrame
    df = pd.DataFrame(data)
    return df

def build_url(report_types=None, start_date=None, end_date=None, topics=None, keywords=None):
    """Constructs the URL with specified filters, including date range in Unix timestamps, and filters English reports."""
    query_params = {
        "text": keywords or "",  # Search keywords
        "f[0]": "language:en",  # Filter for English reports
    }

    # Date range
    if start_date and end_date:
        min_timestamp = date_to_timestamp(start_date)
        max_timestamp = date_to_timestamp(end_date)
        query_params["f[1]"] = f"date:(min:{min_timestamp},max:{max_timestamp})"
    else:
        query_params["f[1]"] = "date:(min:,max:)"

    # Add report types
    index = 2  # Start index for additional filters
    if report_types:
        for report_type in report_types:
            query_params[f"f[{index}]"] = f"report_type:{report_type}"
            index += 1
    # Add topics (sectors)
    if topics:
        for topic in topics:
            query_params[f"f[{index}]"] = f"sector:{topic}"
            index += 1

    return f"{BASE_URL}?{urlencode(query_params, doseq=True)}"

def extract_card_data(card):
    """Extracts data from a single report card."""
    eyebrows_ = card.find_all('fews-taxonomy-eyebrow', slot='eyebrow')

    report_type = eyebrows_[0].text.strip() if len(eyebrows_) > 0 else None
    place = eyebrows_[1].text.strip() if len(eyebrows_) > 1 else None
    date = eyebrows_[2].text.strip() if len(eyebrows_) > 2 else None
    headline = card.get('link-text', '').strip()
    link = f"https://fews.net{card.get('link-href', '').strip()}"
    description_tag = card.find('fews-styled-text', slot='description')
    description = description_tag.text.strip() if description_tag else None

    return {
        'report_type': report_type,
        'place': place,
        'date': date,
        'article_link': link,
        'headline': headline,
        'description': description
    }

def extract_page_data(soup):
    """Extracts data from all report cards on a single page."""
    cards = soup.find_all('fews-card')
    return [extract_card_data(card) for card in cards]

@st.cache_data(show_spinner=False)
def fetch_fewsnet_reports(report_types=None, start_date=None, end_date=None, topics=None, keywords=None):
    """Fetch FEWS NET data with default arguments and validations."""
    # Convert user-friendly text inputs to numeric IDs
    report_types = convert_to_ids(report_types or list(REPORT_TYPE_MAPPING.values()), REPORT_TYPE_MAPPING)
    topics = convert_to_ids(topics or list(TOPIC_MAPPING.values()), TOPIC_MAPPING)

    # Validate the date range
    if end_date:
        validate_date_range(end_date)

    # Build URL with filters and scrape data
    url_with_filters = build_url(report_types, start_date, end_date, topics, keywords)
    report_count = get_report_count(url_with_filters)
    df = scrape_fewsnet(report_types, start_date, end_date, topics, keywords, report_count)
    
    return df

def create_map(df_reports, geojson_data):
    # Load country and capital data
    df_countries = pd.DataFrame(COUNTRIES, columns=['country', 'capital', 'latitude', 'longitude'])

    # Aggregate report types and counts per country
    country_report_info = df_reports.groupby('place').agg({
        'report_type': lambda x: list(x),
        'headline': 'count'
    }).reset_index()

    country_report_info = country_report_info.rename(columns={'headline': 'report_count'})
    country_report_dict = country_report_info.set_index('place').T.to_dict()

    # Create a folium map
    m = folium.Map(location=[20, 0], zoom_start=2)

    # Define color mapping for report types
    report_type_colors = {
        'Targeted Analysis': 'orange',
        'Special Report': 'yellow',
        'Alert': 'red',
        'default': 'gray'
    }

    # Update the style_function
    def style_function(feature):
        country_name = feature['properties'].get('ADMIN', '')
        report_info = country_report_dict.get(country_name, {})
        report_types = report_info.get('report_type', [])
        if report_types:
            if 'Alert' in report_types:
                color = report_type_colors['Alert']
            elif 'Targeted Analysis' in report_types:
                color = report_type_colors['Targeted Analysis']
            elif 'Special Report' in report_types:
                color = report_type_colors['Special Report']
            else:
                color = report_type_colors['default']
        else:
            color = report_type_colors['default']
        return {'fillColor': color, 'color': 'black', 'weight': 1, 'fillOpacity': 0.5}

    # Prepare popup text for each country
    for feature in geojson_data['features']:
        country_name = feature['properties'].get('ADMIN', '').strip()
        report_info = country_report_dict.get(country_name, {})
        report_types = report_info.get('report_type', [])
        report_count = report_info.get('report_count', 0)
        if report_types:
            unique_report_types = ', '.join(set(report_types))
            popup_text = f"<b>{country_name}</b><br>Reports: {report_count}<br>Types: {unique_report_types}"
        else:
            popup_text = f"<b>{country_name}</b>"
        feature['properties']['popup'] = popup_text
        # Add country name as property to capture on click
        feature['properties']['name'] = country_name

    # Add country borders with the updated style_function and popups
    folium.GeoJson(
        geojson_data,
        name='countries',
        style_function=style_function,
        popup=folium.GeoJsonPopup(fields=['popup'], labels=False, localize=True),
        tooltip=folium.GeoJsonTooltip(fields=['ADMIN'], labels=False),
    ).add_to(m)

    # Add markers for each capital city with report counts
    for _, row in df_countries.iterrows():
        country_reports = df_reports[df_reports['place'] == row['country']]
        if not country_reports.empty:
            report_count = len(country_reports)
            report_types = ', '.join(country_reports['report_type'].unique())
            popup_text = f"<b>{row['capital']}</b> ({row['country']})<br>Reports: {report_count}<br>Types: {report_types}"
            first_report_type = country_reports['report_type'].iloc[0]
            marker_color = report_type_colors.get(first_report_type, 'blue')
        else:
            popup_text = f"<b>{row['capital']}</b> ({row['country']})"
            marker_color = 'blue'

        folium.CircleMarker(
            location=[row['latitude'], row['longitude']],
            radius=5,
            popup=folium.Popup(popup_text, max_width=250),
            tooltip=row['capital'],
            color=marker_color,
            fill=True,
            fill_color=marker_color
        ).add_to(m)

    return m

def fewsnet_page():
    st.title("FEWSNET Reports")

    # Filter widgets placed above the map
    st.markdown("### Filters")

    # Arrange filters compactly side by side
    # First row: Report Types and Topics
    col1, col2 = st.columns(2)
    with col1:
        report_type_options = list(REPORT_TYPE_MAPPING.keys())
        selected_report_types = st.multiselect(
            "Select Report Types", options=report_type_options, default=report_type_options
        )
    with col2:
        topic_options = list(TOPIC_MAPPING.keys())
        selected_topics = st.multiselect("Select Topics", options=topic_options)

    # Second row: Start Date, End Date, and Keywords
    col3, col4, col5 = st.columns([1, 1, 2])
    with col3:
        start_date = st.date_input(
            "Start Date",
            value=datetime(2005, 1, 1),
            min_value=datetime(2005, 1, 1),
            max_value=datetime.today()
        )
    with col4:
        end_date = st.date_input(
            "End Date",
            value=datetime.today(),
            min_value=datetime(2005, 1, 1),
            max_value=datetime.today()
        )
    with col5:
        keywords = st.text_input("Keywords")

    # Fetch reports and load GeoJSON data
    with st.spinner("Fetching FEWSNET reports..."):
        df_reports = fetch_fewsnet_reports(
            report_types=selected_report_types,
            start_date=start_date,
            end_date=end_date,
            topics=selected_topics,
            keywords=keywords
        )

    geojson_data = load_geojson()
    gdf_countries = gpd.GeoDataFrame.from_features(geojson_data["features"], crs='epsg:4326')

    # Initialize session state for filtered data
    if 'filtered_df_reports' not in st.session_state:
        st.session_state['filtered_df_reports'] = df_reports.copy()
    if 'clicked_country' not in st.session_state:
        st.session_state['clicked_country'] = None

    # Inject custom CSS to adjust map height and fix multiselect font color
    st.markdown(
        """
        <style>
        iframe {
            height: 600px;
            border-radius: 10px;
        }
        /* Fix font color in multiselect dropdowns */
        div[data-baseweb="select"] span {
            color: black !important;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    try:
        # Create the map
        m = create_map(df_reports, geojson_data)
        # Display the map and capture interactions
        map_data = st_folium(m, width=1200, height=600)

        # Debug: Print the map_data to see what's being returned
        # st.write("Map Data:", map_data)

        # Check if a click occurred
        if map_data and 'last_clicked' in map_data and map_data['last_clicked'] is not None:
            coords = map_data['last_clicked']
            st.write("Clicked Coordinates:", coords)
            point = Point(coords['lng'], coords['lat'])
            # Find the country containing the point
            country = gdf_countries[gdf_countries.contains(point)]
            if not country.empty:
                clicked_country = country.iloc[0]['ADMIN']
                # Filter the dataframe for the selected country
                st.session_state['filtered_df_reports'] = df_reports[df_reports['place'] == clicked_country]
                st.session_state['clicked_country'] = clicked_country
            else:
                st.write("No country found at this location.")
        else:
            # Use the full dataframe if no country is clicked
            st.session_state['filtered_df_reports'] = df_reports.copy()
            st.session_state['clicked_country'] = None

    except Exception as e:
        st.error(f"An error occurred while creating the map: {e}")

    # Add a "Reset Table" button if the table is filtered
    if st.session_state['clicked_country']:
        st.markdown(f"**Showing reports for:** {st.session_state['clicked_country']}")
        if st.button("Reset Table"):
            st.session_state['filtered_df_reports'] = df_reports.copy()
            st.session_state['clicked_country'] = None
    else:
        st.markdown("**Showing all reports**")

    # Display the data table
    st.markdown("### FEWSNET Reports")
    st.dataframe(st.session_state['filtered_df_reports'])

    # Provide input field for report index
    report_index = st.text_input("Enter the serial number of the report you want to chat about:")

    # Add a "Chat" button
    if st.button("Chat"):
        if report_index:
            try:
                # Convert input to integer
                report_index = int(report_index)
                # Check if index is within the DataFrame
                if 0 <= report_index < len(st.session_state['filtered_df_reports']):
                    # Get the selected report
                    selected_report = st.session_state['filtered_df_reports'].iloc[report_index]
                    # Fetch the article content
                    article_content = fetch_report_content(selected_report['article_link'])
                    st.write("Article Content:", article_content)
                    # Store the content in session state
                    st.session_state['article_content'] = article_content
                    st.session_state['article_title'] = selected_report['headline']
                    # Redirect to the chat page
                    st.switch_page("pages/chat.py")
                    # st.rerun()
                else:
                    st.error(f"Please enter a number between 0 and {len(st.session_state['filtered_df_reports']) - 1}.")
            except ValueError:
                st.error("Please enter a valid integer serial number.")
        else:
            st.error("Please enter the serial number of the report.")


if __name__ == "__main__":
    fewsnet_page()
