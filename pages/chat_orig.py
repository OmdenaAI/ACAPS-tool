import streamlit as st
from typing import Generator
from groq import Groq
from langchain_groq import ChatGroq
from datetime import datetime
import gdelt, io, os, time
import pandas as pd
# from modules.sidebar import launch_sidebar
from crewai import Agent, Crew, Task, Process

os.environ["SERPER_API_KEY"] = st.secrets["SERPER_API_KEY"]
os.environ["FIRECRAWL_API_KEY"] = st.secrets["FIRECRAWL_API_KEY"]
from crewai_tools import (
    SerperDevTool,
    ScrapeWebsiteTool,
    tool
)

#os.environ["OPENAI_MODEL_NAME"] = 'gpt-4o-mini'
#os.environ["OPENAI_API_KEY"] = st.secrets["OPENAI_API_KEY"]

# Initialize agents and tools if needed
search_tool = SerperDevTool(n_results=40)
scrape_tool = ScrapeWebsiteTool()

# Existing GDELT tool and fetcher
gd2 = gdelt.gdelt(version=2)  # Initialize GDELT 2.0

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
    if country not in country_code:
      return f"Country '{country}' not found in predefined mappings."
    if keyword not in crisis_cameo_codes:
      return f"Keyword '{keyword}' not recognized. Please provide a valid crisis type."

    try:

        results = gd2.Search([datetime.today().strftime('%Y %m %d')], table='events', coverage=True)

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
        return "Caught an error so please proceed without this data."


@tool
def fetch_gdelt_data(country: str, keyword: str) -> str:
    """
    Fetches and filters GDELT crisis data based on the specified country and crisis keyword.

    Args:
        country (str): The name of the country to filter data for.
        keyword (str): The crisis type keyword (e.g., 'flood', 'earthquake') to filter events.

    Returns:
        str: A string representation of the filtered DataFrame, or a message if no data is found.
    """
    gdelt_df = gdelt_wrapper(country, keyword)
    if gdelt_df.empty:
        return "No data found for specified parameters."
    gdelt_df.to_csv('gdelt_data.csv', index=False)  # Save to CSV
    return gdelt_df.to_string(index=False)  # Return string representation for display

# SeleniumScrapingTool for Web Scraping
#scrape_tool = SeleniumScrapingTool(headless=True)

@tool
def extract_urls_from_gdelt(file_path: str = 'gdelt_data.csv') -> list:
    """
    Extract unique URLs from the GDELT data output file.

    Args:
        file_path (str): The path to the CSV file containing GDELT data.
                         Defaults to 'gdelt_data.csv'.

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
    
# Defining LLM
llm=ChatGroq(temperature=0,
             model_name="groq/llama3-8b-8192",
             api_key=st.secrets["GROQ_API_KEY"])

planner = Agent(
    llm=llm,
    role="Content Planner",
    goal="Plan engaging and factually accurate content on {topic}",
    backstory="You're working on planning a blog article "
              "about the topic: {topic}."
              "You collect information that helps the "
              "audience learn something "
              "and make informed decisions. "
              "Your work is the basis for "
              "the Content Writer to write an article on this topic.",
    allow_delegation=False,
    verbose=True
)

writer = Agent(
    llm=llm,
    role="Content Writer",
    goal="Write insightful and factually accurate "
         "opinion piece about the topic: {topic}",
    backstory="You're working on a writing "
              "a new opinion piece about the topic: {topic}. "
              "You base your writing on the work of "
              "the Content Planner, who provides an outline "
              "and relevant context about the topic. "
              "You follow the main objectives and "
              "direction of the outline, "
              "as provide by the Content Planner. "
              "You also provide objective and impartial insights "
              "and back them up with information "
              "provide by the Content Planner. "
              "You acknowledge in your opinion piece "
              "when your statements are opinions "
              "as opposed to objective statements.",
    allow_delegation=False,
    verbose=True
)

editor = Agent(
    llm=llm,    
    role="Editor",
    goal="Edit a given blog post to align with "
         "the writing style of the organization. ",
    backstory="You are an editor who receives a blog post "
              "from the Content Writer. "
              "Your goal is to review the blog post "
              "to ensure that it follows journalistic best practices,"
              "provides balanced viewpoints "
              "when providing opinions or assertions, "
              "and also avoids major controversial topics "
              "or opinions when possible.",
    allow_delegation=False,
    verbose=True
)

plan = Task(
    description=(
        "1. Prioritize the latest trends, key players, "
            "and noteworthy news on {topic}.\n"
        "2. Identify the target audience, considering "
            "their interests and pain points.\n"
        "3. Develop a detailed content outline including "
            "an introduction, key points, and a call to action.\n"
        "4. Include SEO keywords and relevant data or sources."
    ),
    expected_output="A comprehensive content plan document "
        "with an outline, audience analysis, "
        "SEO keywords, and resources.",
    agent=planner,
)

write = Task(
    description=(
        "1. Use the content plan to craft a compelling "
            "blog post on {topic}.\n"
        "2. Incorporate SEO keywords naturally.\n"
  "3. Sections/Subtitles are properly named "
            "in an engaging manner.\n"
        "4. Ensure the post is structured with an "
            "engaging introduction, insightful body, "
            "and a summarizing conclusion.\n"
        "5. Proofread for grammatical errors and "
            "alignment with the brand's voice.\n"
    ),
    expected_output="A well-written blog post "
        "in markdown format, ready for publication, "
        "each section should have 2 or 3 paragraphs.",
    agent=writer,
)

edit = Task(
    description=("Proofread the given blog post for "
                 "grammatical errors and "
                 "alignment with the brand's voice."),
    expected_output="A well-written blog post in markdown format, "
                    "ready for publication, "
                    "each section should have 2 or 3 paragraphs.",
    agent=editor
)

'''
# Define the GDELT Agent
gdelt_agent = Agent(
            role='Crisis Data Analyst',
            goal="Analyze and report real-time crisis events in specified countries.",
            backstory="An experienced analyst monitoring global crisis events using GDELT data, specializing in detecting and reporting on key crises.",
            tools=[fetch_gdelt_data],
            memory=True,
            verbose=True,
            llm=ChatGroq(api_key=st.secrets["GROQ_API_KEY"], model="groq/llama3-8b-8192")
            #llm=ChatGroq(api_key=st.secrets["GROQ_API_KEY"], model="groq/mixtral-8x7b-32768")
)

        # Define the Scraping Agent
web_scraping = Agent(
            role='Web Scraping Specialist',
            goal="Extract and summarize information from a list of URLs related to crisis events.",
            backstory="A skilled researcher with expertise in extracting and condensing information from online sources.",
            tools=[extract_urls_from_gdelt,scrape_tool],
            memory=True,
            verbose=True,
            llm=ChatGroq(api_key=st.secrets["GROQ_API_KEY"], model_name="groq/llama3-8b-8192")
            #llm=ChatGroq(api_key=st.secrets["GROQ_API_KEY"], model="groq/mixtral-8x7b-32768")
)

        # Define a general conversational Agent
general_agent = Agent(
            role='General Assistant',
            goal="Engage in general conversation and assist the user with various queries.",
            backstory="A friendly assistant ready to help with any question.",
            tools=[],
            memory=True,
            verbose=True,
            llm=ChatGroq(api_key=st.secrets["GROQ_API_KEY"], model="groq/llama3-8b-8192")
            #llm=ChatGroq(api_key=st.secrets["GROQ_API_KEY"], model="groq/mixtral-8x7b-32768")
)
'''

def chat_page():
    st.title("Sophie 👩🏼‍🦰")

    # Initialize the Groq client
    # client = Groq(api_key=st.secrets["GROQ_API_KEY"])

    def kickOff(topic):
        '''
        # Define the GDELT Task
        gdelt_task = Task(
            description=(
                "Retrieve and analyze GDELT data for crises in the specified country and keyword. "
                "Focus on finding recent events related to {keyword} in {country} and prepare a report."
            ),
            expected_output="A formatted report detailing the GDELT events including sources, locations, and actor details.",
            agent=gdelt_agent,
        )

        # Define the General Conversation Task
        general_task = Task(
            description=(
                "Engage in general conversation and provide assistance with any queries or questions by the user."
            ),
            expected_output="Simple answers to general questions or queries.",
            agent=general_agent,
        )

        # Define the Scraping Task
        gdelt_scraping_task = Task(
            description=(
                "Use the URLs provided by the GDELT analysis to extract and summarize their content. "
                "Focus on key details relevant to crisis events. "
                "Your output should be concise and focused on actionable information."
            ),
            expected_output="A summary report based on the provided URL make sure to include URL of the news story.",
            output_file='gdelt.txt',
            create_directory=True,
            agent=web_scraping,
            #inputs={'urls': extract_urls_from_gdelt()}  # Dynamically fetch URLs
        )

        # Assemble the Crew
        sophie_crew = Crew(
            agents=[gdelt_agent, web_scraping, general_agent],
            tasks=[gdelt_task, gdelt_scraping_task, general_task],
            process=Process.sequential,
            # max_rpm=3,
            # manager_agent=manager_agent
        )

        inputs = {
            'country': 'Ukraine',
            'keyword': 'war'
        }
        '''
        sophie_crew = Crew(
            agents=[planner, writer, editor],
            tasks=[plan, write, edit],
            verbose=True
        )

        response = sophie_crew.kickoff(inputs={"topic": topic})
        return response

    # Initialize session state for messages
    if "messages" not in st.session_state:
        # Check if there's article content to include in the context
        if 'article_content' in st.session_state and 'article_title' in st.session_state:
            article_context = f"You have been provided with the following article titled '{st.session_state['article_title']}':\n\n{st.session_state['article_content']}\n\nYou should use this information to answer any questions."
            st.session_state.messages = [
                {"role": "assistant", "content": "Hi, I'm Sophie! You can ask me questions based on the article."},
                {"role": "system", "content": article_context}
            ]
            
            # Clear the article content after using it
            del st.session_state['article_content']
            del st.session_state['article_title']
        else:
            st.session_state.messages = [{"role": "assistant", "content": "Hi, I'm Sophie! How may I help you?"}]

    # Display chat messages from history
    for message in st.session_state.messages:
        if message["role"] in ["assistant", "user"]:
            avatar = '👩🏼‍🦰' if message["role"] == "assistant" else '👨‍💻'
            with st.chat_message(message["role"], avatar=avatar):
                st.markdown(message["content"])

    # User input
    if prompt := st.chat_input("Enter your message here..."):
        st.session_state.messages.append({"role": "user", "content": prompt})

        # Process the input using the crew
        '''task = Task(
            objective=prompt,
            crew=sophie_crew
        )
        task = Task(
            description=prompt,
            agent=general_agent,
            expected_output="A helpful and informative response to the user's query.",
        )'''

        # Get the response from the crew
        response = kickOff(str(prompt))

        # Display the assistant's response
        st.session_state.messages.append({"role": "assistant", "content": response})

        with st.chat_message("assistant", avatar='🤖'):
            st.markdown(response)
            
if __name__ == "__main__":
    chat_page()