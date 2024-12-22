import pandas as pd
import json
import streamlit as st
from modules.actors import *  # Import the scraper functions
from modules.scraper import fetch_main_tweet_dataframe, fetch_comments_dataframe
from modules.utils import (
    load_header,
    is_valid_twitter_url,
    apply_sentiment_pipeline,
    extract_entities_and_relationships,
    create_knowledge_graph
)
from modules.cache_functions import cache_sample_dataset
from modules.graph_functions import *
from modules.acaps import fetch_acaps_data  # Import the ACAPS data fetching function
from modules.agent import run_expert_agent

import pdb

def find_query_data(dataset, query):
    for entry in dataset:
        if entry['query'] == query:
            return entry
    return None

def update_dataframes(df_comments, df_author):
    # Mapping dictionary for sentiment icons and labels
    sentiment_icons = {
        -1: '🔴',
        0: '🟡',
        1: '🟢'
    }
    sentiment_labels = {
        -1: 'Negative',
        0: 'Neutral',
        1: 'Positive'
    }

    with st.spinner("Analyze tweets..."):
        if df_comments is not None and not df_comments.empty:
            # Add Sentiment column based on predictedSentiment
            df_comments['predictedSentiment'] = df_comments['cleaned_text'].apply(lambda x: apply_sentiment_pipeline(x))
            df_comments['Sentiment'] = df_comments['predictedSentiment'].map(sentiment_icons)
            df_comments['sentiment_label'] = df_comments['predictedSentiment'].map(sentiment_labels)
        else:
            st.warning("Comments DataFrame is empty or None!")

        st.session_state["master_df"] = df_comments
        st.session_state["original_tweet"] = df_author


def display_results(selected_actor):
    with st.expander("Tweet Original", expanded=True):
        st.dataframe(
            st.session_state["original_tweet"], height=150, use_container_width=True, key=selected_actor,
        )

    if st.session_state["master_df"].empty:
        st.info("This tweet has no comments to display.")
    else:
        with st.expander("Comments", expanded=True):
            df = st.session_state["master_df"].copy()
            # Ensure Sentiment and sentiment_label columns are at the first positions
            if 'Sentiment' in df.columns and 'sentiment_label' in df.columns:
                cols = ['Sentiment', 'sentiment_label'] + [col for col in df.columns if col not in ['Sentiment', 'sentiment_label']]
                df = df[cols]
            st.dataframe(
                df, height=450, use_container_width=True, key=f'Comments for tweet of {selected_actor}',
            )

        st.write("<br>", unsafe_allow_html=True)

        st.download_button(
            label="Download analyzed comments as JSON",
            data=st.session_state["master_df"].to_json(orient='records').encode('utf-8'),
            file_name="analyzed_comments.json",
            mime="application/json",
            use_container_width=True,
        )

        st.write("<br>", unsafe_allow_html=True)

        st.download_button(
            label="Download as CSV",
            data=st.session_state["master_df"].to_csv(index=False).encode("utf-8"),
            file_name="analyzed_comments.csv",
            use_container_width=True,
        )

# Function to process and display GDELT data
def display_gdelt_data(gdelt_news_data):
    if isinstance(gdelt_news_data, pd.DataFrame):
        if not gdelt_news_data.empty:
            columns_to_display = ['title', 'url', 'sourcecountry']

            # Ensure all required columns are present before filtering
            if all(col in gdelt_news_data.columns for col in columns_to_display):
                gdelt_df_filtered = gdelt_news_data[columns_to_display]
                st.subheader("News Data (from GDELT)")
                st.dataframe(gdelt_df_filtered)
            else:
                st.warning("Some columns are missing in the GDELT data. Available columns: " + ", ".join(
                    gdelt_news_data.columns))
        else:
            st.warning("No GDELT news data available for the selected criteria.")
    else:
        st.error("Unexpected data format for GDELT news data.")

def display_knowledge_graph(text):
    entities, relationships = extract_entities_and_relationships(text)
    create_knowledge_graph(entities, relationships)
    st.components.v1.html(open("knowledge_graph.html").read(), height=600)

def analyse_page():
    load_header("Analysis")

    # Selections
    col1, col2, col3, col4 = st.columns([0.3, 0.3, 0.3, 0.4])
    with col1:
        selected_country = st.selectbox(
            "Select a Country",
            [
                'Afghanistan', 'Albania', 'Algeria', 'Antarctica', 'Antigua And Barbuda', 'Argentina',
                'Australia', 'Austria', 'Azerbaijan', 'Bahamas', 'Bahrain', 'Bangladesh', 'Barbados',
                'Belize', 'Belgium', 'Benin', 'Bermuda', 'Bhutan', 'Bolivia', 'Bosnia-Herzegovina',
                'Botswana', 'Brazil', 'Brunei', 'Bulgaria', 'Burundi', 'Cambodia', 'Cameroon', 'Canada',
                'Chad', 'Chile', 'China', 'Colombia', 'Congo', 'Cook Islands', 'Cuba', 'Cyprus', 'Denmark',
                'Djibouti', 'Dominican Republic', 'Ecuador', 'Egypt', 'El Salvador', 'Eritrea', 'Estonia',
                'Ethiopia', 'Finland', 'France', 'Gambia', 'Gaza Strip', 'Germany', 'Ghana', 'Gibraltar',
                'Greece', 'Grenada', 'Guam', 'Guatemala', 'Guinea', 'Guyana', 'Haiti', 'Honduras', 'Hong Kong',
                'Hungary', 'India', 'Indonesia', 'Iran', 'Iraq', 'Ireland', 'Israel', 'Italy', 'Jamaica',
                'Japan', 'Jersey', 'Jordan', 'Kazakhstan', 'Kenya', 'Kyrgyzstan', 'Laos', 'Latvia', 'Lebanon',
                'Libya', 'Malawi', 'Malaysia', 'Maldives', 'Mali', 'Malta', 'Mauritania', 'Mexico', 'Moldova',
                'Mongolia', 'Montenegro', 'Morocco', 'Namibia', 'Nepal', 'Netherlands', 'New Zealand',
                'Nicaragua', 'Nigeria', 'Niue', 'North Korea', 'Norway', 'Pakistan', 'Palau', 'Panama',
                'Papua New Guinea', 'Peru', 'Philippines', 'Poland', 'Portugal', 'Qatar', 'Rwanda',
                'Saudi Arabia', 'Serbia', 'Singapore', 'South Africa', 'South Korea', 'South Sudan',
                'Spain', 'Sri Lanka', 'Sudan', 'Sweden', 'Switzerland', 'Syria', 'Taiwan', 'Tanzania',
                'Thailand', 'Tonga', 'Turkey', 'Turkmenistan', 'Uganda', 'Ukraine', 'United Arab Emirates',
                'United Kingdom', 'United States', 'Uzbekistan', 'Venezuela', 'Vietnam', 'West Bank', 'Yemen',
                'Zambia', 'Zimbabwe'
            ]
        ).strip()
        st.write(f"Country selected: {selected_country}")

    with col2:
        selected_keyword = st.selectbox(
            "Select a keyword",
            [
                "earthquake",
                "embargo",
                "environmental disaster",
                "epidemic",
                "ethnic cleansing",
                "famine",
                "financial crisis",
                "flood",
                "hurricane",
                "health crisis",
                "hostage situation",
                "kidnapping",
                "landslide",
                "martial law",
                "military conflict",
                "pandemic",
                "political instability",
                "protests",
                "riots",
                "state of emergency",
                "terrorist attack",
                "chemical spill",
                "nuclear incident",
                "violent repression",
                "war",
                "wildfire",
                "tornado",
                "tsunami",
                "biological threat",
                "blockade",
                "economic crisis"
            ]
        ).strip()
        st.write(f"Keyword selected: {selected_keyword}")

    with col3:
        st.write("<br>", unsafe_allow_html=True)
        analyze_button = st.button("Analyze", use_container_width=True)

    with col4:
        start_date = st.date_input("Start Date", key="start_date")
        end_date = st.date_input("End Date", key="end_date")
        st.write(f"Date Range: {start_date} to {end_date}")

    # Bind the "Analyze" button to run Apify actors
    if analyze_button:
        with st.spinner("Fetching data from API actors..."):
            acaps_data = fetch_acaps_data(selected_country)
            twitter_data = run_apify_twitter_actor(selected_country, selected_keyword, start_date, end_date)
            google_trends_data, gdelt_news_data = run_apify_actors(selected_country, selected_keyword)

            # Store results
            st.session_state['acaps_data'] = acaps_data
            st.session_state['twitter_data'] = twitter_data
            st.session_state['google_trends_data'] = google_trends_data
            st.session_state['gdelt_news_data'] = gdelt_news_data

            # Process Google trends data if exists
            if google_trends_data:
                queries = set([val['query'] for val in google_trends_data])
                filtered_searches = llama_filter_chatgroq(queries)
                st.session_state['filtered_searches'] = filtered_searches

    # Display data if available
    if 'acaps_data' in st.session_state:
        st.subheader("ACAPS Risk List Data", divider='rainbow')
        if not st.session_state['acaps_data'].empty:
            st.dataframe(st.session_state['acaps_data'])
        else:
            st.warning("No ACAPS data available.")

    if 'twitter_data' in st.session_state:
        st.subheader("Twitter Data", divider='rainbow')
        if not st.session_state['twitter_data'].empty:
            st.dataframe(st.session_state['twitter_data'])
            twitter_data_json = st.session_state['twitter_data'].to_json(orient='records')
            twitter_text = " ".join([tweet["text"] for tweet in json.loads(twitter_data_json)])
            display_knowledge_graph(twitter_text)
        else:
            st.warning("No Twitter data available.")

    if 'google_trends_data' in st.session_state:
        if st.session_state['google_trends_data']:
            st.subheader("Google Trends Searches", divider='rainbow')
            filtered_searches = st.session_state.get('filtered_searches', {})
            if filtered_searches:
                description_key = list(filtered_searches.keys())[0]
                st.dataframe(pd.DataFrame(filtered_searches[description_key]))

                filtered_queries = [k['query'] for k in filtered_searches[description_key]]
                for i, target_query in enumerate(filtered_queries):
                    result = find_query_data(st.session_state['google_trends_data'], target_query)
                    st.markdown(f"\nQuery: {target_query}")
                    expander = st.expander("See query trend")
                    if result is not None and 'articles' in result:
                        df_articles = pd.DataFrame(result['articles'])
                        # Ensure 'timeAgo' and 'snippet' exist before dropping
                        drop_cols = [col for col in ['timeAgo', 'snippet'] if col in df_articles.columns]
                        df_articles = df_articles.drop(columns=drop_cols, errors='ignore')
                        expander.write(df_articles)
                        if 'exploreLink' in result:
                            expander.write(result['exploreLink'])
                    else:
                        expander.write("No article data available for this query.")

    if 'gdelt_news_data' in st.session_state:
        st.subheader("GDELT Search", divider='rainbow')
        st.dataframe(st.session_state['gdelt_news_data'])

    # If we have all required data, show the "Generate Expert Context and Prediction" button
    if ('twitter_data' in st.session_state and
        'google_trends_data' in st.session_state and
        'gdelt_news_data' in st.session_state and
        'acaps_data' in st.session_state and
        selected_country and selected_keyword):

        google_trends_data_json = json.dumps(st.session_state['google_trends_data'])
        gdelt_data_json = st.session_state['gdelt_news_data'].to_json(orient='records')
        acaps_data_json = st.session_state['acaps_data'].to_json(orient='records')
        serper_query = f"{selected_country} {selected_keyword} crisis after:{start_date.strftime('%Y-%m-%d')} before:{end_date.strftime('%Y-%m-%d')}"

        if st.button("Generate Expert Context and Prediction"):
            with st.spinner("Generating context and prediction..."):
                result = run_expert_agent(
                    twitter_data_json,
                    google_trends_data_json,
                    gdelt_data_json,
                    acaps_data_json,
                    serper_query,
                    start_date.strftime("%Y-%m-%d"),  # Convert start_date to string format
                    end_date.strftime("%Y-%m-%d")     # Convert end_date to string format
                )
                st.session_state['expert_result'] = result

                # Ensure result is a string
                if isinstance(result, dict):
                    result = json.dumps(result)

    # Tweet URL input
    cols = st.columns([5, 1])
    if 'twitter_url' not in st.session_state:
        st.session_state['twitter_url'] = ''
    if 'df_comments' not in st.session_state:
        st.session_state['df_comments'] = None
    if 'df_author' not in st.session_state:
        st.session_state['df_author'] = None

    with cols[0]:
        twitter_url = st.text_input("Tweet URL:", value=st.session_state['twitter_url']).strip()
    with cols[1]:
        st.write("<br>", unsafe_allow_html=True)
        submitted_twitter = st.button("Submit", use_container_width=True, key='twitter_input')

    # Google Trends URL input
    cols = st.columns([5, 1])
    with cols[0]:
        gtrend_url = st.text_input("Google Trends URL:").strip()
    with cols[1]:
        st.write("<br>", unsafe_allow_html=True)
        submitted_gtrends = st.button("Submit", use_container_width=True, key='gtrends_input')

    if submitted_gtrends:
        records = google_trends_for_url(gtrend_url)
        plot_google_trends(records)

    valid_twitter = is_valid_twitter_url(twitter_url)

    if submitted_twitter:
        if not valid_twitter:
            st.toast("⚠️ Invalid URL. Please enter a valid Twitter URL", type="error")
        else:
            with st.spinner("Obtaining data..."):
                df_author = fetch_main_tweet_dataframe(twitter_url)
                df_comments = fetch_comments_dataframe(twitter_url)
                st.session_state['df_author'] = df_author
                st.session_state['df_comments'] = df_comments
                update_dataframes(df_comments, df_author)

    if st.session_state.get('df_author') is not None and st.session_state.get('df_comments') is not None:
        display_results('Actor Selected')
