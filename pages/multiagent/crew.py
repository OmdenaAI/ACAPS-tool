from crewai import Agent, Task, Crew, Process
from pydantic import Field, BaseModel
from typing import List
from typing_extensions import TypedDict
from langchain_core.output_parsers import StrOutputParser, JsonOutputParser
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from pages.multiagent.pdf_writer import generate_pdf
from pages.multiagent.extra_tools import (
    search_wikipedia,
    scrap_webpage,
    fetch_reliefweb_reports,
    fetch_country_specific_reliefweb_reports,
    fetch_fewsnet_reports,
    fetch_country_specific_fewsnet_reports,
    fetch_acled_data,
    fetch_gdelt_data,
    extract_urls_from_gdelt,
    fetch_twitter_data,
    extract_text_from_twitter,
    google_trending_searches,
    filter_trends_query,
    scrape_tool
)
import os, json
import streamlit as st

class Paragraph(TypedDict):
    sub_header: str
    paragraph: str

class Essay(BaseModel):
    header: str = Field(..., description="The header of the essay")
    entry: str = Field(..., description="The entry of the essay")
    paragraphs: List[Paragraph] = Field(..., description="The paragraphs of the essay")
    conclusion: str = Field(..., description="The conclusion of the essay")
    summary: str = Field(..., description="The summary of the essay")
    seo_keywords: List[str] = Field(..., description="The SEO keywords of the essay")

class CrewClass:
    """Dynamic Crew Class with Intent Recognition and Agent Selection"""
    def __init__(self, llm):
        self.llm = llm

        os.environ["OPENAI_API_KEY"] = st.secrets["OPENAI_API_KEY"]
        os.environ["OPENAI_MODEL_NAME"] = 'gpt-4o-mini'

        # Initialize Agents
        self.initialize_agents()

        # Initialize Tasks
        self.initialize_tasks()
        self.essay_content = ""
        self.model = ChatOpenAI(model="gpt-4o-mini", api_key=st.secrets["OPENAI_API_KEY"])

    def initialize_agents(self):
        # General Agent
        self.general_agent = Agent(
            role="General Chatbot",
            goal="Engage in general conversation and answer user queries.",
            backstory="You are a friendly and helpful chatbot that assists users with various queries or engages in small talk as needed.",
            verbose=True,
            memory=True,
        )

        # Researcher
        self.researcher = Agent(
            role="Content Researcher",
            goal="Research accurate content on a given topic.",
            backstory="You're researching content to write an essay about a topic provided by the user."
                      "You collect information that helps the audience learn something and make informed decisions."
                      "Your work is the basis for the Content Writer to write an article on this topic.",
            verbose=True,
            tools=[search_wikipedia, scrap_webpage],
            memory=True,
        )

        # Writer
        self.writer = Agent(
            role="Content Writer",
            goal="Write insightful and factually accurate content.",
            backstory="You're working on writing an essay about a topic provided by the user."
                      "You base your writing on the research provided by the Content Researcher."
                      "You follow the main objectives and direction of the outline, as provided by the Content Researcher."
                      "You also provide objective and impartial insights and back them up with information provided by the Content Researcher.",
            verbose=True,
            memory=True,
        )

        # Editor
        self.editor = Agent(
            role="Content Editor",
            goal="Edit a given essay to align with the writing style of the organization.",
            backstory="You are an editor who receives an essay from the Content Writer."
                      "Your goal is to review the essay to ensure that it follows best practices, provides insights, and balanced viewpoints"
                      "when providing opinions or assertions, and also avoids major controversial topics or opinions when possible.",
            verbose=True,
            memory=True,
        )

        # ReliefWeb Agent
        self.reliefweb_agent = Agent(
            role="ReliefWeb Reports Analyst",
            goal="Analyze the latest ReliefWeb reports and provide detailed insights.",
            backstory="You are an analyst who fetches ReliefWeb reports using the 'fetch_reliefweb_reports' tool."
                      "Your goal is to analyze these reports and help the audience make informed decisions."
                      "Your insights on these reports are the basis for the chatbot to answer user's queries.",
            verbose=True,
            memory=True,
            tools=[fetch_reliefweb_reports],
        )

        # Country Specific ReliefWeb Agent
        self.country_specific_reliefweb_agent = Agent(
            role="ReliefWeb Country-Specific Reports Analyst",
            goal="Analyze the ReliefWeb reports of the country {country} and provide detailed insights.",
            backstory="You are an analyst who fetches ReliefWeb reports using the 'fetch_country_specific_reliefweb_reports' tool."
                      "Your goal is to analyze these reports and help the audience make informed decisions."
                      "Your insights on these reports are the basis for the chatbot to answer user's queries.",
            verbose=True,
            memory=True,
            tools=[fetch_country_specific_reliefweb_reports],
        )

        # FEWSNET Agent
        self.fewsnet_agent = Agent(
            role="FEWSNET Reports Analyst",
            goal="Analyze the latest FEWSNET reports and provide detailed insights.",
            backstory="You are an analyst who fetches FEWSNET reports using "
                      "the 'fetch_fewsnet_reports' tool to fetch a certain number of latest reports."
                      "Your goal is to analyze these reports and help the audience make informed decisions."
                      "Your insights on these reports are the basis for the chatbot to answer user's queries.",
            verbose=True,
            memory=True,
            tools=[fetch_fewsnet_reports],
        )

        # Country Specific FEWSNET Agent
        self.country_specific_fewsnet_agent = Agent(
            role="FEWSNET Country-Specific Reports Analyst",
            goal="Analyze the latest FEWSNET reports of {country} and provide detailed insights.",
            backstory="You are an analyst who fetches FEWSNET reports using "
                      "the 'fetch_country_specific_fewsnet_reports' to fetch country-specific reports for {country}."
                      "Your goal is to analyze these reports and help the audience make informed decisions."
                      "Your insights on these reports are the basis for the chatbot to answer user's queries.",
            verbose=True,
            memory=True,
            tools=[fetch_country_specific_fewsnet_reports],
        )

        # GDELT Agent
        self.gdelt_agent = Agent(
            role='Crisis Data Analyst',
            goal="Analyze and report real-time crisis events in specified countries.",
            backstory="An experienced analyst monitoring global crisis events using GDELT data, specializing in detecting and reporting on key crises.",
            tools=[fetch_gdelt_data],
            memory=True,
            verbose=True,
        )

        # Web Scraping Agent
        self.web_scraping_agent = Agent(
            role='Web Scraping Specialist',
            goal="Extract and summarize information from a list of URLs related to crisis events.",
            backstory="A skilled researcher with expertise in extracting and condensing information from online sources.",
            tools=[extract_urls_from_gdelt, scrape_tool],
            memory=True,
            verbose=True,
        )

        # Twitter Agent
        self.twitter_agent = Agent(
            role='Social Media Analyst',
            goal="Analyze and report trends from Twitter based on keywords and countries.",
            backstory="A skilled social media analyst specializing in tracking trends and extracting key insights from tweets.",
            tools=[fetch_twitter_data],
            memory=True,
            verbose=True,
        )

        # Define the Summarizer Agent
        self.twitter_summariser_agent = Agent(
            role='Twitter Summariser Agent',
            goal="Extract and summarize information from a list of URLs related to crisis events.",
            backstory="A skilled researcher with expertise at collection and analysing twitter conversations.",
            tools=[extract_text_from_twitter],
            memory=True,
            verbose=True,
        )

        # Google Trends Agent
        self.google_trends_agent = Agent(
            role="Google Trends Analyst",
            goal="Fetch and analyze Google Trends data for specific countries.",
            backstory="An expert in using Google Trends data to identify significant trends.",
            tools=[google_trending_searches],
            verbose= True,
            memory= True,
        )

        self.trends_analysis_agent = Agent(
            role="Trends Analysis Specialist",
            goal="Filter Google Trends data for crisis-relevant insights.",
            backstory="An AI-powered assistant specializing in data refinement and crisis identification. ",
            tools=[filter_trends_query,scrape_tool],
            verbose= True,
            memory= True,
        )

        self.acled_data_analysis_agent = Agent(
            role="ACLED Data Analyst",
            goal="Fetch and analyze ACLED data for the country {country}.",
            backstory="An expert in analyzing ACLED data to identify significant crisis events. ",
            tools=[fetch_acled_data],
            verbose= True,
            memory= True,
        )

    def initialize_tasks(self):
        # General Task
        self.general_task = Task(
            description="Engage in conversation with the user, providing helpful and friendly responses.",
            expected_output="Appropriate responses to user inputs, maintaining conversational context.",
            agent=self.general_agent,
        )

        # Research Task
        self.research_task = Task(
            description=(
                "Research and gather information on the provided topic. "
                "Prioritize the latest trends, key players, and noteworthy news."
                "Identify the target audience, considering their interests and pain points."
                "Include SEO keywords and relevant data or sources."
            ),
            expected_output="A comprehensive document with an outline, audience analysis, SEO keywords, and resources.",
            tools=[search_wikipedia, scrap_webpage],
            agent=self.researcher,
        )

        # Write Task
        self.write_task = Task(
            description=(
                "Use the research content to craft a compelling essay. "
                "Incorporate SEO keywords naturally."
                "Ensure the essay is structured with an engaging introduction, insightful body, and a summarizing conclusion."
                "Proofread for grammatical errors and alignment with the brand's voice."
                "Pick a suitable header."
            ),
            expected_output="A well-written essay in markdown format, ready for publication.",
            context=[self.research_task],
            agent=self.writer,
        )

        # Edit Task
        self.edit_task = Task(
            description="Proofread the given essay for grammatical errors and alignment with the brand's voice.",
            expected_output="A polished essay in required format, ready for publication.",
            output_json=Essay,
            context=[self.write_task],
            agent=self.editor,
        )

        # ReliefWeb Task
        self.reliefweb_task = Task(
            description="Fetch and analyze the latest ReliefWeb reports.",
            expected_output="A comprehensive report of key findings and insights from individual ReliefWeb reports."
                            "Do NOT use # or ## or ### for any headers. Use the '####' format or even lighter for headers and sub-headers."
                            "Include relevant links if and wherever possible. Ensure that the links are not fake or lead to Error 404.",
            agent=self.reliefweb_agent,
        )

        # Country Specific ReliefWeb Task
        self.country_specific_reliefweb_task = Task(
            description="Fetch and analyze the latest ReliefWeb reports for the country {country}.",
            expected_output="A comprehensive report of key findings and insights from individual ReliefWeb reports."
                            "Do NOT use # or ## or ### for any headers. Use the '####' format or even lighter for headers and sub-headers."
                            "Include relevant links if and wherever possible. Ensure that the links are not fake or lead to Error 404.",
            agent=self.country_specific_reliefweb_agent,
        )

        # FEWSNET Task
        self.fewsnet_task = Task(
            description="Fetch and analyze the latest FEWSNET reports.",
            expected_output="A comprehensive report of key findings and insights from individual FEWSNET reports."
                            "Do NOT use # or ## or ### for any headers. Use the '####' format or even lighter for headers and sub-headers."
                            "Include relevant links if and wherever possible. Ensure that the links are not fake or lead to Error 404.",
            agent=self.fewsnet_agent,
        )

        # Country Specific FEWSNET Task
        self.country_specific_fewsnet_task = Task(
            description="Fetch and analyze the latest FEWSNET reports for the country {country}.",
            expected_output="A comprehensive report of key findings and insights from individual FEWSNET reports."
                            "Do NOT use # or ## or ### for any headers. Use the '####' format or even lighter for headers and sub-headers."
                            "Include relevant links if and wherever possible. Ensure that the links are not fake or lead to Error 404.",
            agent=self.country_specific_fewsnet_agent,
        )

        # GDELT Task
        self.gdelt_task = Task(
            description="Fetch and analyze real-time crisis data from GDELT for the country {country} and keyword {keyword}.",
            expected_output="A report on significant crisis events detected in the specified country.",
            agent=self.gdelt_agent,
        )

        # Web Scraping Task
        self.web_scraping_task = Task(
            description="Extract and summarize information from provided URLs related to crisis events.",
            expected_output="A concise summary of information extracted from the URLs.",
            agent=self.web_scraping_agent,
        )

        # Twitter Analysis Task
        self.twitter_scraping_task = Task(
            description=(
                "Scrape Twitter for tweets related to {keyword} in {country}. "
                "Analyze the data and provide a summary of the most relevant and popular tweets."
            ),
            expected_output="A summary of tweets.",
            agent=self.twitter_agent,
            inputs={'keyword': '{keyword}', 'country': '{country}'},
        )

        # Define the Twitter Summary Task
        self.twitter_summary = Task(
            description=(
                "Use the text provided by the Twitter analysis to extract and summarize their content. "
                "Focus on key details relevant to crisis events do not include any extra information, do not mention any names in the final output, but cite the URL that it was taken from"
                "Your output should be concise and focused on actionable information."
            ),
            expected_output="A summary report based on the twitter text.",
            output_file='twitter_summary.txt',
            create_directory=True,
            agent=self.twitter_summariser_agent,
        )

        # Google Trends Task
        self.fetch_trends_task = Task(
            description="Fetch trending searches from Google Trends for {country}.",
            expected_output="A list of trending searches with metadata.",
            agent=self.google_trends_agent,
            create_directory=True
        )

        self.trends_analysis_task = Task(
            description="Based on the google trends dataframe, make sure to scrape related URL and provide summary of the same",
            expected_output="A highly comprehensive report on the identified trends and significant search queries, "
                            "with relevant links and statistics included. Do NOT use # or ## or ### for any headers. "
                            "Use the '####' format or even lighter for headers and sub-headers if any.",
            agent=self.trends_analysis_agent,
            output_file='gtrends_summary.txt',
            create_directory=True,
        )

        # ACLED Task
        self.acled_data_analysis_task = Task(
            description="Fetch and analyze ACLED data for the country {country}.",
            expected_output="A report on significant crisis events detected in the specified country.",
            agent=self.acled_data_analysis_agent,
        )


    # Function to parse user input and extract intent and parameters
    def parse_user_input(self, user_input):
        memory = st.session_state.memory.load_memory_variables({})
        prompt = f"""
            You are an assistant that extracts intent and parameters from user input.

            \nConversation History: {memory}
            \n\nUser Input: "{user_input}"

            Identify the user's intent accurately and extract relevant parameters if any.\n
            Sidenote: \n
            1.  If you think the intent should be 'general_talk',
                please double check if any other possible intent suits well.\n
            2.  If you think the intent should be 'request_latest_reports',
                please double check if 'general_talk' suits better, especially
                because if the word latest is not in user's input prompt
                then it would likely mean that the user is asking for something 
                from the conversation history and you can pass it to 'general_talk'.\n

            Possible intents (in order of priority):
            - inquire_country_status
            - request_latest_reports
            - write_report
            - general_talk

            For each intent, extract parameters as needed:
            - inquire_country_status: country, keyword
            - request_latest_reports: country, number_of_reports
            - write_report: topic

            Respond in JSON format like:
            {{
                "intent": "intent_name",
                "parameters": {{
                    "country": "country_name",
                    "number_of_reports": integer,
                    "keyword": "keyword",
                    "topic": "topic_name"
                }}
            }}
            """
        response = self.llm(prompt).content
        response = response[response.index("{") : response.rindex("}")+1]
        print(response)
        try:
            data = json.loads(response)
        except json.JSONDecodeError:
            # If parsing fails, default to general_query
            data = {"intent": "general_talk", 
                    "parameters": {}}
        print("data\n", data)
        intent = data.get('intent', 'general_talk')
        parameters = data.get('parameters', {})
        return intent, parameters

    # Function to handle general queries
    def handle_general_query(self, user_input):
        simple_answer_prompt = """
                            You are an expert and you are providing simple reponses to the user's texts.
                            
                            \nConversation History: {memory}
                            \nTopic: {user_input}
                            """
        prompt = PromptTemplate.from_template(simple_answer_prompt)
        memory = st.session_state.memory.load_memory_variables({})
        chain = prompt | self.model | StrOutputParser()
        result = chain.invoke({"user_input": user_input, "memory": memory})
        self.essay_content = str(memory)
        return result[4:] if result.startswith("AI: ") else result

    # Function to handle inquiries about country status
    def handle_country_inquiry(self, country, keyword):
        # Decide which agents and tasks to use
        agents = [self.country_specific_reliefweb_agent, 
                  self.country_specific_fewsnet_agent,
                  self.gdelt_agent,
                  self.web_scraping_agent,
                  self.acled_data_analysis_agent,
                  self.twitter_agent,
                  self.twitter_summariser_agent,
                  self.google_trends_agent,] 
                  #self.trends_analysis_agent]
        
        tasks = [self.country_specific_reliefweb_task, 
                 self.country_specific_fewsnet_task,
                 self.gdelt_task,
                 self.web_scraping_task, 
                 self.acled_data_analysis_task,
                 self.twitter_scraping_task,
                 self.twitter_summary,
                 self.fetch_trends_task,]
                 #self.trends_analysis_task]
        
        agent_input = {"country": country, 
                       "keyword": keyword}

        # Create a crew with the selected agents and tasks
        crew = Crew(
            agents=agents,
            tasks=tasks,
            process=Process.sequential,
            manager_llm=self.llm,
            verbose=True,
            memory=True,
        )

        results = crew.kickoff(agent_input)
        response = self.generate_combined_response(results)
        return response

    # Function to handle requests for latest reports
    def handle_latest_reports_request(self, country, number_of_reports):
        crew = Crew(
            agents=[self.reliefweb_agent, self.fewsnet_agent],
            tasks=[self.reliefweb_task, self.fewsnet_task],
            process=Process.sequential,
            verbose=True,
            memory=True,
        )

        results = crew.kickoff({
                        'country': country,
                        'number_of_reports': number_of_reports
                    })
        
        response = self.generate_report_summaries(results)
        return response

    # Function to handle requests to write a report  
    def handle_write_report(self):
        print("**REPORT GENERATION**")

        if not self.essay_content:
            return {"response": "Oopsies! I can't make a report of nothing, right? You need to ask me to do some analysis first."}

        # Use the LLM to convert the essay into the Essay JSON format
        parser = JsonOutputParser(pydantic_object=Essay)
        prompt = PromptTemplate(
            template=(
                "Convert the following essay into the given JSON format and return the new JSON file ONLY."
                "Do NOT exclude any information given to you.\n"
                "\nThe Essay Content:\n{essay_content}"
                "\n{format_instructions}"
            ),
            input_variables=["essay_content"],
            partial_variables={"format_instructions": parser.get_format_instructions()},
        )

        chain = prompt | self.model | parser
        formatted_essay = chain.invoke({"essay_content": self.essay_content})
        # print("**ESSAY CONTENT**\n", self.essay_content, "\n**FORMATTED ESSAY**\n", formatted_essay)
        pdf_name = generate_pdf(formatted_essay)

        return {"response": "Here is your report!", "pdf_name": f"{pdf_name}", "essay": formatted_essay}


    def generate_combined_response(self, crew_output):
        response = "Here is the latest information:\n"
        # print("Task output: \n", crew_output.tasks_output)
        # print("JSON: \n", crew_output.json())
        # Extract outputs from crew_output.tasks_output
        for task_output in crew_output.tasks_output:
            agent_name = task_output.agent  # Get the agent's role as the name
            content = task_output#.output         # Get the output from the agent
            response += f"\n**{agent_name}:**\n{content}\n"
            # response += f"\n{content}\n"

        self.essay_content = response

        answer_combination_prompt = """
                            You are an expert at formatting and re-structuring texts. The below text is most likely disorganized and mis-formatted.
                            You are required to properly organize and format the text and give a well structured markdown response to the user. 
                            You must NOT mix up everything but keep information from each agent/analyst separate.
                            Also, do NOT alter or omit any of the information and links contained in the text. 
                            Also, ensure that your markdown response has headers with hierarchial levels from #### and below, and no # or ## or ### headers used.
                            
                            \n\nThe text: {text}
                            """
        prompt = PromptTemplate.from_template(answer_combination_prompt)
        chain = prompt | self.model | StrOutputParser()
        result = chain.invoke({"text": response})

        return (response, result)

    def generate_report_summaries(self, crew_output):
        response = "Here are the latest reports:\n"

        # Extract outputs from crew_output.tasks_output
        for task_output in crew_output.tasks_output:
            agent_name = task_output.agent
            content = task_output 
            response += f"\n**{agent_name}:**\n{content}\n"

        self.essay_content = response
        return response

    # Main function to process user input
    def ultimate_kickoff(self, user_input, essay=""):
        intent, params = self.parse_user_input(user_input)
        print(f"Intent: '{intent}'")

        if intent == 'general_talk':
            return self.handle_general_query(user_input)

        elif intent == 'inquire_country_status':
            country = params.get('country', 'Ukraine')
            keyword = params.get('keyword', 'war')
            return self.handle_country_inquiry(country, keyword)

        elif intent == 'request_latest_reports':
            country = params.get('country', 'Ukraine')
            number_of_reports = params.get('number_of_reports', 15)
            return self.handle_latest_reports_request(country, number_of_reports)

        elif intent == 'write_report':
            return self.handle_write_report()

        else:
            return "I did not get your intent. Please rephrase your query."