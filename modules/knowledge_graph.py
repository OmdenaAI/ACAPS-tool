import streamlit as st
from pyvis.network import Network
import networkx as nx
import json
from streamlit.components.v1 import html

from crewai_tools import ScrapeWebsiteTool
from crewai import Agent, Task, Crew, Process
from crewai_tools import tool
from datetime import datetime
import gdelt
import io
import pandas as pd
import spacy
from openai import OpenAI
# Existing GDELT tool and fetcher
gd2 = gdelt.gdelt(version=2)  # Initialize GDELT 2.0

nlp = spacy.load("en_core_web_sm")
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

            return gdelt_df[['SOURCEURL', 'ActionGeo_FullName', 'CAMEOCodeDescription', 'GoldsteinScale', 'Actor1Name',
                             'Actor1CountryCode', 'Actor2Name', 'Actor2CountryCode', 'NumMentions', 'NumArticles']]
    except Exception as e:
        print(e)


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


scrape_tool = ScrapeWebsiteTool()

# Define the GDELT Agent
gdelt_agent = Agent(
    role='Crisis Data Analyst',
    goal="Analyze and report real-time crisis events in specified countries.",
    backstory="An experienced analyst monitoring global crisis events using GDELT data, specializing in detecting and reporting on key crises.",
    tools=[fetch_gdelt_data],
    memory=True,
    verbose=True,
    #llm=ChatGroq(temperature=0, model_name="groq/llama3-8b-8192")
)

# Define the Scraping Agent
web_scraping = Agent(
    role='Web Scraping Specialist',
    goal="Extract and summarize information from a list of URLs related to crisis events.",
    backstory="A skilled researcher with expertise in extracting and condensing information from online sources.",
    tools=[extract_urls_from_gdelt, scrape_tool],
    memory=True,
    verbose=True,
    #llm=ChatGroq(temperature=0, model_name="groq/llama3-8b-8192")
)

# Define the GDELT Task
gdelt_task = Task(
    description=(
        "Retrieve and analyze GDELT data for crises in the specified country and keyword. "
        "Focus on finding recent events related to {keyword} in {country} and prepare a report."
    ),
    expected_output="A formatted report detailing the GDELT events including sources, locations, and actor details.",
    agent=gdelt_agent

)

# Define the Scraping Task
gdelt_scraping_task = Task(
    description=(
        "Use the URLs provided by the GDELT analysis to extract and summarize their content. "
        "Focus on key details relevant to crisis events. "
        "Your output should be concise and focused on actionable information."
    ),
    expected_output="A summary report based on the provided URL make sure to include URL of the news story along with the brief story.",
    output_file='gdelt.txt',
    create_directory=True,
    agent=web_scraping,
    #inputs={'urls': extract_urls_from_gdelt()}  # Dynamically fetch URLs
)

# Update the Crew with the new agent and task
gdelt_crew = Crew(
    agents=[gdelt_agent, web_scraping],
    tasks=[gdelt_task, gdelt_scraping_task],
    process=Process.sequential,  # Sequential execution
)


def extract_relationships(file_path: str, model: str = "gpt-4o-mini") -> str:
    """
    Extracts triples (subject, relationship, object) from the provided file.

    Args:
        file_path (str): Path to the .txt or .csv file.
        model (str): OpenAI model to use for extraction (default is gpt-4o-mini).

    Returns:
        str: JSON-formatted triples as a string.
    """
    system_message = """Extract all relationships between entities in context. 
    Return only triples in JSON format, e.g., 
    [{"subject": "Trump", "relationship": "beat", "object": "Harris"}]
    """

    # Read input file
    if file_path.endswith(".txt"):
        with open(file_path, "r") as file:
            input_text = file.read()
    elif file_path.endswith(".csv"):
        df = pd.read_csv(file_path)
        input_text = df.to_string(index=False)
    else:
        raise ValueError("Unsupported file format. Use .txt or .csv.")

    # Call OpenAI API
    client = OpenAI()
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": system_message},
            {"role": "user", "content": f"Context:\n{input_text}"}
        ],
        max_tokens=1000,
        temperature=0
    )

    response_content = response.choices[0].message.content.strip()
    print(f"Raw Response Content: {response_content}")  # Debugging print

    # Strip Markdown delimiters if present
    if response_content.startswith("```json"):
        response_content = response_content[7:]  # Remove the opening ```json
    if response_content.endswith("```"):
        response_content = response_content[:-3]  # Remove the closing ```

    # Validate JSON content
    try:
        triples = json.loads(response_content)
        return json.dumps(triples, indent=2)  # Return pretty JSON
    except json.JSONDecodeError as e:
        raise ValueError("Failed to parse response as JSON.") from e



from pyvis.network import Network
import networkx as nx
import json
import streamlit as st

# Function to assign colors based on entity type
def get_color(entity: str) -> str:
    type_to_color = {
        "person": "#6495ED",  # Blue
        "location": "#3CB371",  # Green
        "organization": "#CD5C5C",  # Red
        "event": "#F4A460",  # Orange
        "media": "#6A5ACD"  # Purple
    }

    # Process the entity with spaCy to determine its type
    # Load spaCy's small English model

    doc = nlp(entity)
    for ent in doc.ents:
        if ent.label_ == "PERSON":
            return type_to_color["person"]
        elif ent.label_ == "GPE" or ent.label_ == "LOC":
            return type_to_color["location"]
        elif ent.label_ == "ORG":
            return type_to_color["organization"]
        elif ent.label_ == "EVENT":
            return type_to_color["event"]
    return "#D3D3D3"  # Default gray for unknown types

def get_size(entity: str) -> int:
    """Assigns node size based on entity type."""

    doc = nlp(entity)
    for ent in doc.ents:
        if ent.label_ == "PERSON":
            return 30
        elif ent.label_ == "GPE" or ent.label_ == "LOC":
            return 30
        elif ent.label_ == "ORG":
            return 30
        elif ent.label_ == "EVENT":
            return 30
    return 15  # Default size

def knowledge_graph_tool(triples_data: str) -> str:
    """
    Creates an interactive knowledge graph from relationship triples, displays it inline, and embeds a legend.

    Args:
        triples_data (str): JSON string containing triples of subject, relationship, and object.

    Returns:
        str: Path to the saved interactive graph as an HTML file.
    """
    try:
        triples = json.loads(triples_data)
    except json.JSONDecodeError:
        return "Invalid JSON input. Ensure the format is correct."

    if not all('subject' in t and 'relationship' in t and 'object' in t for t in triples):
        return "Each triple must contain 'subject', 'relationship', and 'object' fields."

    # Create a directed graph
    G = nx.DiGraph()

    for item in triples:
        subject = item['subject']
        relationship = item['relationship']
        obj = item['object']

        G.add_node(subject, title=subject, color=get_color(subject), size=get_size(subject), label=subject)
        G.add_node(obj, title=obj, color=get_color(obj), size=get_size(obj), label=obj)
        G.add_edge(subject, obj, title=relationship, weight=4)

    # Use pyvis for visualization
    net = Network(notebook=True, height="800px", width="100%", directed=True, cdn_resources='in_line')
    net.from_nx(G)
    net.show_buttons(filter_=['physics'])

    # Embed a legend directly into the HTML of the graph
    legend_html = """
    <div style="position:absolute;top:10px;left:10px;background-color:white;padding:10px;border-radius:5px;box-shadow:0px 0px 10px rgba(0,0,0,0.1);z-index:10;">
        <h4>Legend</h4>
        <ul>
            <li><span style='color:#6495ED;'>Person</span></li>
            <li><span style='color:#3CB371;'>Location</span></li>
            <li><span style='color:#CD5C5C;'>Organization</span></li>
            <li><span style='color:#F4A460;'>Event</span></li>
            <li><span style='color:#6A5ACD;'>Media Channel</span></li>
        </ul>
    </div>
    """
    # Insert the legend HTML into the graph's HTML structure
    net.html += legend_html

    output_path = "interactive_knowledge_graph.html"
    net.save_graph(output_path)

    return output_path
