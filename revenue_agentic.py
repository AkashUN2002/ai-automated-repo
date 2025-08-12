from crewai import Crew, Agent, Task, LLM, Process
import configparser
import os
from dotenv import load_dotenv
load_dotenv()
from crewai_tools import CodeInterpreterTool

csv_file_path=r"C:\Users\Akash UN\Desktop\Revenue_Growth_Agentic\sample\merged_dataset.csv"

config = configparser.ConfigParser()
config.read('agent_config.ini')

openai_api_key = config['API_KEY']['openai_api_key']
# os.environ["OPENAI_API_KEY"]=openai_api_key
from pydantic import BaseModel, Field
from typing import Type
from crewai.tools import BaseTool
import pandas as pd
from langchain_experimental.agents import create_pandas_dataframe_agent
from langchain.llms import OpenAI

llm = OpenAI(temperature=0)

# # Create the CSV agent
df=pd.read_csv(csv_file_path)
agent = create_pandas_dataframe_agent(
    llm,
    df,
    verbose=True,
    allow_dangerous_code=True
)
response = agent.invoke("Which year did jurasic park film release?")
print(response['output'])

# df_1 = df[["Age", "Fare"]]
# df_2 = df[["Fare", "Survived"]]

# tool = PythonAstREPLTool(locals={"df_1": df_1, "df_2": df_2})
# llm_with_tool = llm.bind_tools(tools=[tool], tool_choice=tool.name)
# df_template = """```python
# {df_name}.head().to_markdown()
# >>> {df_head}
# ```"""
# df_context = "\n\n".join(
#     df_template.format(df_head=_df.head().to_markdown(), df_name=df_name)
#     for _df, df_name in [(df_1, "df_1"), (df_2, "df_2")]
# )

# system = f"""You have access to a number of pandas dataframes. \
# Here is a sample of rows from each dataframe and the python code that was used to generate the sample:

# {df_context}

# Given a user question about the dataframes, write the Python code to answer it. \
# Don't assume you have access to any libraries other than built-in Python ones and pandas. \
# Make sure to refer only to the variables mentioned above."""
# prompt = ChatPromptTemplate.from_messages([("system", system), ("human", "{question}")])

# chain = prompt | llm_with_tool | parser | tool
# chain.invoke(
#     {
#         "question": "return the difference in the correlation between age and fare and the correlation between fare and survival"
#     }
# )
        
# # class CSVReaderInput(BaseModel):
# #     """Schema for CSV Reader Tool input."""
# #     file_path: str = Field(..., description="The path to the CSV file to be read.")

# class CSVReaderTool(BaseTool):
#     name: str = "csv_reader"
#     description: str = "Reads a CSV file from the specified file path and returns its content as a DataFrame."
#     # args_schema: Type[CSVReaderInput] = CSVReaderInput
#     file_path:str=""
#     def __init__(self,path):
#         super().__init__()
#         self.file_path=path

#     def _run(self) -> pd.DataFrame:
#         """Reads the CSV file and returns its content."""
#         try:
#             df = pd.read_csv(self.file_path)
#             return df  # Convert DataFrame to string for display
#         except Exception as e:
#             return f"Error reading CSV file: {e}"

# csv_tool=CSVReaderTool(csv_file_path)
# agentic_llm=LLM(
#     model="gpt-4o",
#     temperature=0.7,        # Higher for more creative outputs
#     timeout=120,           # Seconds to wait for response
#     max_tokens=4000,       # Maximum length of response
#     top_p=0.9,            # Nucleus sampling parameter
#     frequency_penalty=0.1, # Reduce repetition
#     presence_penalty=0.1,  # Encourage topic diversity
#     seed=42,               # For reproducible results
#     api_key=openai_api_key
# )

# project_manager_agent=Agent(
#     role="Agent Network Manager",
#     goal="Efficiently manage the team of agents and ensure high quality task completion. Your primary goal is to coordinate all agents effectively to maximize productivity, ensuring each agent is actively contributing to achieve the best possible output.",
#     backstory="You are an experienced project manager known for managing complex projects and orchestrating seamless teamwork among a diverse team of agents. Your expertise lies in maximizing resource efficiency, utilizing each agent's strengths, and upholding high standards for collaboration and task completion.",
#     tools=[],
#     allow_delegation=True,
#     verbose=True,
#     llm=agentic_llm
# )
# data_analyst_agent = Agent(
#     role="Data Analyst",
#     goal="Aggregate and analyze both internal and external data—such as Excel reports, database extracts, and web data—to derive actionable insights on prices, sales, and promotions. Use these insights to support revenue optimization strategies. To query from CSV/EXCEL files, use the python compiler to accept the dataframe of pandas and compile the python code with the dataframe and then return the response",
#     backstory="You are a seasoned data analyst with deep expertise in data mining, statistical analysis, and visualization. With a keen eye for detail, you extract valuable insights from various data formats, including spreadsheets and database queries, to inform strategic decisions that drive revenue growth.",
#     tools=[csv_tool,CodeInterpreterTool()],
#     allow_delegation=False,
#     verbose=True,
#     llm=agentic_llm
# )

# description='''Conduct an in-depth analysis of historical sales data from all regions to identify the location that has collectively generated the highest total revenue over the last fiscal period. Your analysis should:
# Aggregate sales figures across all product categories for each region.
# Compare the total revenue figures to determine the region with the highest sales.
# Highlight any significant trends or anomalies that might explain why a particular region outperformed others.
# Provide insights on factors that could be driving high sales in that region, such as market conditions, promotional activities, or demographic factors.
# The final output should be a well-organized report that includes a data table summarizing the total sales per region, clear identification of the top-performing region, and a concise narrative explaining your findings.'''
# expected_output='''A clear statement identifying the region with the highest sales, for example:
# "Based on the analysis, Asia is the region with the highest total sales, generating $1,500,000 in revenue."
# A narrative commentary that briefly explains possible reasons for this outcome, such as:
# "The superior sales performance in Asia may be attributed to strong market demand, effective local promotions, and an expanding customer base in emerging markets. Additionally, the region's diverse product mix appears to have resonated well with local consumer preferences'''

# task=Task(
#     description=description,
#     expected_output=expected_output
# )

# crew=Crew(
#     agents=[data_analyst_agent],
#     verbose=True,
#     process=Process.hierarchical,
#     manager_agent=project_manager_agent,
#     tasks=[task]
# )
# output=crew.kickoff()
# print(output)


