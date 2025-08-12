from dotenv import load_dotenv
load_dotenv()
import configparser
config = configparser.ConfigParser()
config.read('agent_config.ini')
openai_api_key = config['API_KEY']['openai_api_key']
from phi.model.openai import OpenAIChat
from phi.tools.newspaper4k import Newspaper4k
from phi.tools.googlesearch import GoogleSearch
from phi.tools.duckdb import DuckDbTools
from phi.tools.duckduckgo import DuckDuckGo
from phi.tools.file import FileTools

from phi.agent import Agent
from phi.agent.duckdb import DuckDbAgent
from pathlib import Path
import os
base_dir=Path(r"C:\Users\Akash UN\Desktop\Revenue_Growth_Agentic\sample")

companydata=[{"data_name":"Cpmpany data",
              "complete_data":r"C:\Users\Akash UN\Desktop\Revenue_Growth_Agentic\sample\sales_data.csv"}]


file_save_agent=Agent(
    name="File save agent",
    role="Write data to a doc or word file",
    tools=[FileTools(base_dir=base_dir)]
)
webagent = Agent(
    name="Business and Tech Web Research Expert",
    role="Conduct comprehensive web research exclusively on companies, brands, products, financial markets, and technology. Focus on gathering detailed and reliable data on corporate performance, market trends, product specifications, financial reports, and technical innovations.",
    # model=OpenAIChat(id="gpt-4o",openai_api_key=openai_api_key),
    tools=[DuckDuckGo()],
    instructions=[
        "1. Prioritize retrieving information on companies, including their market performance, financial reports, recent corporate news, strategic initiatives, and competitive positioning.",
        "2. Focus on product-related research by gathering detailed specifications, feature comparisons, pricing data, user reviews, and performance metrics.",
        "3. For brands, compile data on reputation, marketing strategies, target audiences, and global presence.",
        "4. When exploring financial information, concentrate on stock performance, earnings reports, revenue trends, and investment insights.",
        "5. Include technical details and analysis for technology-related products or services, highlighting innovation, development trends, and competitive analysis.",
        "6. Ensure all gathered information is from credible and verifiable sources, and always include proper citations.",
        "7. Exclude topics unrelated to business, finance, products, brands, or technology, such as politics, entertainment, or general lifestyle content."
    ],
    show_tool_calls=True,
    markdown=True,
)

dataanalyst = Agent(
    name="Company Data Analyst Agent",
    role="Analyze and derive insights exclusively from company data, focusing on key financial metrics, market performance, and strategic indicators. Generate clear, understandable graphs and visualizations to support the analysis.",
    # model=OpenAIChat(id="gpt-4o", openai_api_key=openai_api_key),
    tools=[DuckDbTools()],
    instructions=[
        "COMPANY DATA"+str(companydata),
        "1. Focus solely on analyzing company data provided by the organization. Prioritize financial metrics, revenue trends, market performance, expenses, profitability, and growth rates.",
        "2. Extract actionable insights such as key performance indicators (KPIs), significant trends, anomalies, and strategic implications from the data.",
        "3. Generate clear and well-labeled graphs and visualizations (compulsory) (e.g., line charts, bar graphs, pie charts, scatter plots) to effectively present trends, comparisons, and insights.",
        "4. Provide detailed explanations for each analysis step, including the methodologies, assumptions, and any limitations encountered during the analysis.",
        "5. Summarize findings in clear, concise language, ensuring that the insights are understandable to stakeholders with varying levels of technical expertise.",
        "6. Ensure that all outputs, including graphs and analysis, are based exclusively on the company data provided, and refrain from incorporating unrelated data sources.",
        "7. Validate your findings by cross-referencing multiple data points within the dataset, and include proper annotations and citations where applicable."
    ],
    show_tool_calls=True,
    markdown=True,
)

agent_team = Agent(
    name="Analyst Team",
    team=[webagent, dataanalyst,file_save_agent],
    # model=OpenAIChat(id="gpt-4o", openai_api_key=openai_api_key),
    # role="Team Leader for Coordinated Business and Data Analysis",
    instructions=[
        "1. On receiving a user query, first, analyze the company data, include maximum graphical data as possible, then assess if the task involves web-based research, financial or company data analysis, or a combination of both. Compulsorly answer the question based on the organization (company) data only.",
        "2. First always work on the company analysis part, after which you would get certain data which is company specific, which can be delegated to the web search agent if further data in needed.",
        "3. Integrate and compile the results and analysis done and save all the data with all the graphs to a word file.",
        "4. Always include proper sources and citations for all data provided.",
        "5. Present data in a clear, structured manner using tables and graphs whenever applicable.",
        "6. Ensure the final output is detailed, understandable, and actionable for stakeholders."
        "7. Save the generated report along with all the graphs to a word file document."
    ],
    show_tool_calls=True,
    markdown=True,
)

agent_team.print_response("Give me an analysis on my sales.", stream=True)



























# from phi.agent import Agent
# from phi.tools.hackernews import HackerNews
# from phi.tools.duckduckgo import DuckDuckGo
# from phi.tools.newspaper4k import Newspaper4k

# hn_researcher = Agent(
#     name="HackerNews Researcher",
#     role="Gets top stories from hackernews.",
#     tools=[HackerNews()],
# )

# web_searcher = Agent(
#     name="Web Searcher",
#     role="Searches the web for information on a topic",
#     tools=[DuckDuckGo()],
#     add_datetime_to_instructions=True,
# )

# article_reader = Agent(
#     name="Article Reader",
#     role="Reads articles from URLs.",
#     tools=[Newspaper4k()],
# )

# hn_team = Agent(
#     name="Hackernews Team",
#     team=[hn_researcher, web_searcher, article_reader],
#     instructions=[
#         "First, search hackernews for what the user is asking about.",
#         "Then, ask the article reader to read the links for the stories to get more information.",
#         "Important: you must provide the article reader with the links to read.",
#         "Then, ask the web searcher to search for each story to get more information.",
#         "Finally, provide a thoughtful and engaging summary.",
#     ],
#     show_tool_calls=True,
#     markdown=True,
# )
# hn_team.print_response("Write an article about the top 2 stories on hackernews", stream=True)