from dotenv import load_dotenv
load_dotenv()
# import json
# from phi.model.openai import OpenAIChat
# from phi.agent.duckdb import DuckDbAgent
import configparser
config = configparser.ConfigParser()
config.read('agent_config.ini')

openai_api_key = config['API_KEY']['openai_api_key']

# data_analyst = DuckDbAgent(
#     model=OpenAIChat(model="gpt-4o",openai_api_key=openai_api_key),
#     semantic_model=json.dumps(
#         {
#             "tables": [
#                 {
#                     "name": "inventory",
#                     "description": "Contains information about the products, stock quantity, price etc.",
#                     "path": r"C:\Users\Akash UN\Desktop\Revenue_Growth_Agentic\sample\retail_inventory_large.csv"
#                 }
#             ]
#         }
#     ),
#     markdown=True,
# )
# data_analyst.print_response(
#     "Which movies have the best rating?",
#     stream=True,
# )

# from phi.agent import Agent
# from phi.model.openai import OpenAIChat
# from phi.tools.yfinance import YFinanceTools

# finance_agent = Agent(
#     name="Finance Agent",
#     model=OpenAIChat(id="gpt-4o",openai_api_key=openai_api_key),
#     tools=[YFinanceTools(stock_price=True, analyst_recommendations=True, company_info=True, company_news=True, technical_indicators=True,key_financial_ratios=True, income_statements=True, stock_fundamentals=True)],
#     instructions=["Use tables to display data"],
#     show_tool_calls=True,
#     markdown=True,
# )
# finance_agent.print_response("Search through the indian stocks which is providing the maximum returns and give an analysis on the stock along with the recommendation to either buy it or not.", stream=True)

# from phi.model.openai import OpenAIChat
# from phi.agent import Agent
# from phi.tools.exa import ExaTools

# globe_hopper_agent = Agent(
#     name="Globe Hopper",
#     model=OpenAIChat(id="gpt-4o",openai_api_key=openai_api_key),
#     tools=[ExaTools()],
#     markdown=True,
#     description="You are an expert itinerary planning agent. Your role is to assist users in creating detailed, customized travel plans tailored to their preferences and needs.",
#     instructions=[
#         "Use Exa to search and extract relevant data from reputable travel platforms.",
#         "Collect information on flights, accommodations, local attractions, and estimated costs from these sources.",
#         "Ensure that the gathered data is accurate and tailored to the user's preferences, such as destination, group size, and budget constraints.",
#         "Create a clear and concise itinerary that includes: detailed day-by-day travel plan, suggested transportation and accommodation options, activity recommendations (e.g., sightseeing, dining, events), an estimated cost breakdown (covering transportation, accommodation, food, and activities).",
#         "If a particular website or travel option is unavailable, provide alternatives from other trusted sources.",
#         "Do not include direct links to external websites or booking platforms in the response."
#     ],
# )

# globe_hopper_agent.print_response(
#     "I want to plan a trip for 3 people for 2 days (11th March and 13th March) in Phuket within 15K INR. Please suggest options for places to stay, activities, and a detailed itinerary for these 2 days with transportation, activities and food",
#     stream=True,
# )

from phi.agent import Agent
from phi.model.openai import OpenAIChat
from phi.storage.agent.sqlite import SqlAgentStorage
from phi.tools.duckduckgo import DuckDuckGo
from phi.tools.yfinance import YFinanceTools
from phi.playground import Playground, serve_playground_app

web_agent = Agent(
    name="Web Agent",
    model=OpenAIChat(id="gpt-4o"),
    tools=[DuckDuckGo()],
    instructions=["Always include sources"],
    storage=SqlAgentStorage(table_name="web_agent", db_file="agents.db"),
    add_history_to_messages=True,
    markdown=True,
)

finance_agent = Agent(
    name="Finance Agent",
    model=OpenAIChat(id="gpt-4o"),
    tools=[YFinanceTools(stock_price=True, analyst_recommendations=True, company_info=True, company_news=True)],
    instructions=["Use tables to display data"],
    storage=SqlAgentStorage(table_name="finance_agent", db_file="agents.db"),
    add_history_to_messages=True,
    markdown=True,
)

app = Playground(agents=[finance_agent, web_agent]).get_app()

if __name__ == "__main__":
    serve_playground_app("playground:app", reload=True, host='8000')