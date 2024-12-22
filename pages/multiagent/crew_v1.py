from crewai import Agent, Task, Crew, Process
from pydantic import BaseModel, Field
from typing import List
from typing_extensions import TypedDict
import streamlit as st
import os
from langchain_groq import ChatGroq
from pages.multiagent.extra_tools import (
    search_wikipedia, 
    scrap_webpage, 
    fetch_reliefweb_reports, 
    fetch_fewsnet_reports,
    fetch_gdelt_data,
    extract_urls_from_gdelt,
    fetch_twitter_data,
    extract_text_from_twitter,
    google_trending_searches,
    filter_trends_query,
    scrape_tool
)

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
    """Essay Writing Crew Class"""
    def __init__(self, llm):
        self.llm = llm
        
        os.environ["OPENAI_API_KEY"] = st.secrets["OPENAI_API_KEY"]
        os.environ["OPENAI_MODEL_NAME"] = 'gpt-4o-mini'

        self.researcher = Agent(
            role="Researcher",
            goal="Research accurate content on {topic}",
            backstory="You're researching content to write an essay about the topic: {topic}."
                      "You collect information that helps the audience learn something and make informed decisions."
                      "Your work is the basis for the Content Writer to write an article on this topic.",
            verbose=True,
            # llm=ChatGroq(model="groq/llama3-groq-70b-8192-tool-use-preview", api_key=st.secrets["GROQ_API_KEY_2"])
        )

        self.writer = Agent(
            role="Writer",
            goal="Write insightful and factually accurate content."
                 "opinion piece about the provided topic",
            backstory="You're working on writing a new opinion piece about the provided topic."
                      "You base your writing on the work of the Content Researcher, who provides an outline and relevant context about the topic."
                      "You follow the main objectives and direction of the outline, as provide by the Content Researcher."
                      "You also provide objective and impartial insights and back them up with information provide by the Content Researcher.",
            verbose=True,
            # llm=ChatGroq(model="groq/llama3-groq-70b-8192-tool-use-preview", api_key=st.secrets["GROQ_API_KEY_2"])
        )
        self.editor = Agent(
            role="Editor",
            goal="Edit a given essay to align with the writing style of the organization.",
            backstory="You are an editor who receives an essay either from the Content Writer or the Master Agent."
                      "Your goal is to review the essay to ensure that it follows best practices, provides insights, and balanched viewpoints"
                      "when providing opinions or assertions,and also avoids major controversial topics or opinions when possible.",
            verbose=True,
            # llm=ChatGroq(model="groq/llama3-groq-70b-8192-tool-use-preview", api_key=st.secrets["GROQ_API_KEY_2"])
        )

        # ReliefWeb Agent
        self.reliefweb_agent = Agent(
            role="ReliefWeb Analyst",
            goal="Analyze the latest ReliefWeb reports and provide detailed insights.",
            backstory="You are an analyst who fetches ReliefWeb reports using the 'fetch_reliefweb_reports' tool that is provided."
                      "Your goal is to analyze these reports and help the audience make informed decisions."
                      "Your insights on these reports are the basis for the Master Agent to write an essay and answer user's queries.",
            verbose=True,
            memory=True,
            # llm=ChatGroq(model="groq/llama3-groq-70b-8192-tool-use-preview", api_key=st.secrets["GROQ_API_KEY_2"])
        )

        self.master_agent = Agent(
            role="Master Agent",
            goal="Write a comprenesive and factually accurate content based on the insights from the Analyst.",
            backstory="You're working on writing a comprehensive detailed report-type essay based on the insights from the Analyst."
                      "You base your writing on the work of the Analyst in your crew, who provides an outline and relevant insights about the report(s)."
                      "You follow the main objectives and direction of the outline, as provide by the Analyst."
                      "You also provide objective and impartial insights and back them up with information provide by the Analyst.",
            verbose=True,
            memory=True,
            # llm=ChatGroq(model="groq/llama3-groq-70b-8192-tool-use-preview", api_key=st.secrets["GROQ_API_KEY_2"])
        )

        # FEWSNET Agent
        self.fewsnet_agent = Agent(
            role="FEWSNET Analyst",
            goal="Analyze the latest FEWSNET reports and provide detailed insights.",
            backstory="You are an analyst who fetches FEWSNET reports using the 'fetch_fewsnet_reports' tool that is provided."
                      "Your goal is to analyze these reports and help the audience make informed decisions."
                      "Your insights on these reports are the basis for the Master Agent to write an essay and answer user's queries.",
            verbose=True,
            memory=True,
            # llm=ChatGroq(model="groq/llama3-groq-70b-8192-tool-use-preview", api_key=st.secrets["GROQ_API_KEY_2"])
        )

        # Define the GDELT Agent
        self.gdelt_agent = Agent(
            role='Crisis Data Analyst',
            goal="Analyze and report real-time crisis events in specified countries.",
            backstory="An experienced analyst monitoring global crisis events using GDELT data, specializing in detecting and reporting on key crises.",
            tools=[fetch_gdelt_data],
            memory=True,
            verbose=True,
            # llm=ChatGroq(model="groq/llama3-groq-70b-8192-tool-use-preview", api_key=st.secrets["GROQ_API_KEY_2"])
        )

        # Define the Scraping Agent
        self.web_scraping = Agent(
            role='Web Scraping Specialist',
            goal="Extract and summarize information from a list of URLs related to crisis events.",
            backstory="A skilled researcher with expertise in extracting and condensing information from online sources.",
            tools=[extract_urls_from_gdelt, scrape_tool],
            memory=True,
            verbose=True,
            # llm=ChatGroq(model="groq/llama3-groq-70b-8192-tool-use-preview", api_key=st.secrets["GROQ_API_KEY_2"])
        )

        # Define the Twitter Agent
        self.twitter_agent = Agent(
            role='Social Media Analyst',
            goal="Analyze and report trends from Twitter based on keywords and countries.",
            backstory="A skilled social media analyst specializing in tracking trends and extracting key insights from tweets.",
            tools=[fetch_twitter_data],
            memory=True,
            verbose=True,
            # llm=ChatGroq(model="groq/llama3-groq-70b-8192-tool-use-preview", api_key=st.secrets["GROQ_API_KEY_2"])
        )

        # Define the Summarizer Agent
        self.twitter_summariser_agent = Agent(
            role='Web Scraping Specialist',
            goal="Extract and summarize information from a list of URLs related to crisis events.",
            backstory="A skilled researcher with expertise at collection and analysing twitter conversations.",
            tools=[extract_text_from_twitter],
            memory=True,
            verbose=True,
            # llm=ChatGroq(model="groq/llama3-groq-70b-8192-tool-use-preview", api_key=st.secrets["GROQ_API_KEY_2"])
        )

        self.google_trends_agent = Agent(
            role="Google Trends Analyst",
            goal="Fetch and analyze Google Trends data for specific countries.",
            backstory="An expert in using Google Trends data to identify significant trends.",
            tools=[google_trending_searches],
            verbose= True,
            memory= True,
            # llm=ChatGroq(model="groq/llama3-groq-70b-8192-tool-use-preview", api_key=st.secrets["GROQ_API_KEY_2"])
        )

        self.trends_analysis_agent = Agent(
            role="Trends Analyst",
            goal="Filter Google Trends data for crisis-relevant insights.",
            backstory="An AI-powered assistant specializing in data refinement and crisis identification. ",
            tools=[filter_trends_query, scrape_tool],
            verbose= True,
            memory= True,
            # llm=ChatGroq(model="groq/llama3-groq-70b-8192-tool-use-preview", api_key=st.secrets["GROQ_API_KEY_2"])
        )

        self.research = Task(
            description=(
                "1. Prioritize the latest trends, key players, and noteworthy news on {topic}.\n"
                "2. Identify the target audience, considering their interests and pain points.\n"
                "3. Research a detailed content outline including an introduction, key points, and a conclusion.\n"
                "4. Include SEO keywords and relevant data or sources."
            ),
            expected_output="A comprehensive document with an outline, audience analysis, SEO keywords, and resources.",
            tools = [search_wikipedia, scrap_webpage],
            agent=self.researcher,
        )

        self.write = Task(
            description=(
                "1. Use the content to craft a compelling essay.\n"
                "2. Incorporate SEO keywords naturally.\n"
                "3. Sections/Subtitles are properly named in an engaging manner.\n"
                "4. Ensure the essay is structured with an engaging introduction, insightful body, and a summarizing conclusion.\n"
                "5. Proofread for grammatical errors and alignment with the brand's voice.\n"
                "6. Pick a suitable header\n"
            ),
            expected_output="A well-written essay in markdown format, ready for publication, each section should have 2 or 3 paragraphs.",
            context=[self.research],
            agent=self.writer,
        )

        # ReliefWeb Task
        self.reliefweb_task = Task(
            description=(
                "1. Fetch the latest {number_of_reports} ReliefWeb report(s) using the 'fetch_reliefweb_reports' tool provided."
                    "Use the given 'search_wikipedia' tool as secondary to search for relevant additional information on the topics in the reports."
                    "Do NOT use wikipedia to fetch data or do research on data that is not available in the reports.\n"
                "2. Analyze these reports, extract key information and help the audience make informed decisions.\n"
                "3. Research a detailed content outline including an introduction, insightful key points, and a conclusion.\n"
                "4. Include SEO keywords and relevant data or sources.\n"
                "5. Do NOT mix all the reports together, analyze each report separately and provide insights for each report."
                    "Please include the original title and date of the report in its analysis.\n"
            ),
            expected_output="A comprehensive analytical report based on the latest ReliefWeb information.",
            tools=[fetch_reliefweb_reports, search_wikipedia],
            agent=self.reliefweb_agent,
        )

        # FEWSNET Task
        self.fewsnet_task = Task(
            description=(
                "1. Fetch the latest {number_of_reports} FEWSNET report(s) using the 'fetch_fewsnet_reports' tool provided."
                    "Use the given 'search_wikipedia' tool as secondary to search for relevant additional information on the topics in the reports."
                    "Do NOT use wikipedia to fetch data or do research on data that is not available in the reports.\n"
                "2. Analyze these reports, extract key information and help the audience make informed decisions.\n"
                "3. Research a detailed content outline including an introduction, insightful key points, and a conclusion.\n"
                "4. Include SEO keywords and relevant data or sources.\n"
                "5. Do NOT mix all the reports together, analyze each report separately and provide insights for each report."
                    "Please include the original title and date of the report in its analysis.\n"
            ),
            expected_output="A comprehensive analytical report based on the latest FEWSNET information.",
            tools=[fetch_fewsnet_reports, search_wikipedia],
            agent=self.fewsnet_agent,
        )

        self.edit = Task(
            description="Proofread the given essay for grammatical errors and alignment with the brand's voice.",
            expected_output="A well-written essay in required format, ready for publication, each section should have 2 or 3 paragraphs.",
            output_json = Essay,
            context=[self.write],
            agent=self.editor
        )

        # Define the GDELT Task
        self.gdelt_task = Task(
            description=(
                "Retrieve and analyze GDELT data for crises in the specified country and keyword. "
                "Focus on finding recent events related to {keyword} in {country} and prepare a report."
            ),
            expected_output="A formatted report detailing the GDELT events including sources, locations, and actor details.",
            agent=self.gdelt_agent
        )

        # Define the Scraping Task
        self.gdelt_scraping_task = Task(
            description=(
                "Use the URLs provided by the GDELT analysis to extract and summarize their content. "
                "Focus on key details relevant to crisis events. "
                "Your output should be concise and focused on actionable information."
            ),
            expected_output="A summary report based on the provided URL make sure to include URL of the news story.",
            output_file='gdelt.txt',
            create_directory=True,
            agent=self.web_scraping,
        )

        # Define the Twitter Task
        self.twitter_scraping_task = Task(
            description=(
                "Scrape Twitter for tweets related to {keyword} in {country}. "
                "Analyze the data and provide a summary of the most relevant and popular tweets."
            ),
            expected_output="A summary of tweets.",
            agent=self.twitter_agent,
            inputs={'keyword': '{keyword}', 'country': '{country}'},
        )

        # Define the Scraping Task
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
            #inputs={'urls': extract_urls_from_gdelt()}  # Dynamically fetch URLs
        )

        self.fetch_trends_task = Task (
            description="Fetch trending searches from Google Trends for {country}.",
            expected_output="A list of trending searches with metadata.",
            agent=self.google_trends_agent,
            create_directory=True
        )

        self.trends_analysis_task = Task (
            description="Based on the gtrends dataframe, make sure to scrape related URL and provide summary of the same",
            expected_output="A filtered list of crisis-relevant trends with descriptions.",
            agent=self.trends_analysis_agent,
            output_file='gtrends_summary.txt',
            create_directory=True,
        )

        # Master Agent Task
        self.masteragent_task = Task(
            description="1. Use the content to craft a factually correct report."
                            "Do NOT mix all the reports together (if there are many), instead give analysis of each report separately."
                            "Also, please include the original title and date of the report in its analysis.\n"
                        "2. Incorporate SEO keywords naturally.\n"
                        "3. Sections/Subtitles are properly named in an engaging manner.\n"
                        "4. Ensure the essay is structured with an engaging introduction, insightful body, a key points section and a summarizing conclusion.\n"
                        "5. Proofread for grammatical errors.\n"
                        "6. Pick a suitable header that represents all the fetched reports.\n"
                        "7. Do not use the # or ## while writing the header in markdown. "
                            "Always use ### for the header and other lower heading levels for other titles and subtitles considering their hierarchy.\n",
            expected_output="A comprehensive report with facts and insights, ready for publication.",
            agent=self.master_agent,
            # context=[self.reliefweb_task, self.fewsnet_task, self.gdelt_task, self.gdelt_scraping_task, self.twitter_scraping_task, self.twitter_summary, self.fetch_trends_task, self.trends_analysis_task]
        )

        # General Chatbot
        self.general_agent = Agent(
            role="Manager",
            goal="Manage the crew and ensure that the tasks are completed efficiently.",
            backstory="You are a superb manager who prioritizes time but also takes care of"
                    "the precise and factual nature of the reply.."
                    "You manage the crew and ensure that the tasks are completed efficiently."
                    "Do not take very long to reply to the user. If the user is just engaging in small talk,"
                    "then reply youself, without any delay." 
                    "Be quick and precise.",
            verbose=True,
            memory=True,
            # llm=ChatGroq(model="groq/llama3-groq-70b-8192-tool-use-preview", api_key=st.secrets["GROQ_API_KEY_2"])
        )

        # General Chatbot Task
        self.general_task = Task(
            description="Answer user queries and provide general information.",
            expected_output="Responses to user texts like daily talk.",
            agent=self.general_agent,
        )

    def kickoff(self,*args):
        return Crew(
            agents=[self.researcher, self.writer, self.editor],
            tasks=[self.research, self.write, self.edit],
            process=Process.sequential,
            verbose=True,
            memory=True
        ).kickoff(*args)

    def reliefweb_kickoff(self, *args):
        # Update the task description with the number of reports
        # self.reliefweb_task.description = self.reliefweb_task.description.format(number_of_reports=number_of_reports)
        # Create a crew with only the ReliefWeb agent and task
        return Crew(
            agents=[self.reliefweb_agent, self.master_agent],
            tasks=[self.reliefweb_task, self.masteragent_task],
            process=Process.sequential,
            verbose=True,
            memory=True
        ).kickoff(*args)
    
    def fewsnet_kickoff(self, *args):
        # Update the task description with the number of reports
        # self.fewsnet_task.description = self.fewsnet_task.description.format(number_of_reports=number_of_reports)
        # Create a crew with only the FEWS NET agent and task
        return Crew(
            agents=[self.fewsnet_agent, self.master_agent],
            tasks=[self.fewsnet_task, self.masteragent_task],
            process=Process.sequential,
            verbose=True,
            memory=True
        ).kickoff(*args)
    
    def crisis_kickoff(self, *args):
        return Crew(
            agents=[self.gdelt_agent, 
                    self.web_scraping, 
                    self.twitter_agent, 
                    self.twitter_summariser_agent, 
                    self.google_trends_agent, 
                    self.trends_analysis_agent
                ],
            tasks=[self.gdelt_task, 
                   self.gdelt_scraping_task, 
                   self.twitter_scraping_task,
                   self.twitter_summary, 
                   self.fetch_trends_task, 
                   self.trends_analysis_task
                ],
            process=Process.sequential,
            verbose=True,
            memory=True
        ).kickoff(*args)

    def gdelt_kickoff(self, *args):
        return Crew(
            agents=[self.gdelt_agent, self.web_scraping, self.master_agent],
            tasks=[self.gdelt_task, self.gdelt_scraping_task, self.masteragent_task],
            process=Process.sequential,
            verbose=True,
            memory=True
        ).kickoff(*args)
    
    def google_trends_kickoff(self, *args):
        return Crew(
            agents=[self.google_trends_agent, self.trends_analysis_agent, self.master_agent],
            tasks=[self.fetch_trends_task, self.trends_analysis_task, self.masteragent_task],
            process=Process.sequential,
            verbose=True,
            memory=True
        ).kickoff(*args)
    
    def ultimate_kickoff(self, *args):
        return Crew(
            agents=[self.reliefweb_agent, self.fewsnet_agent, self.master_agent,
                    self.gdelt_agent, self.web_scraping, 
                    self.twitter_agent, self.twitter_summariser_agent,
                    self.google_trends_agent, self.trends_analysis_agent
                ],
            tasks=[self.reliefweb_task, self.fewsnet_task, self.masteragent_task,
                   self.gdelt_task, self.gdelt_scraping_task, 
                   self.twitter_scraping_task, self.twitter_summary,
                   self.fetch_trends_task, self.trends_analysis_task
                ],
            process=Process.hierarchical,
            manager_agent=self.general_agent,
            planning_llm=self.llm,
            verbose=True,
            memory=True
        ).kickoff(*args)