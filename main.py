from dotenv import load_dotenv
import os
import pandas as pd

from llama_index.experimental.query_engine import PandasQueryEngine
from llama_index.core.tools import QueryEngineTool, ToolMetadata
from llama_index.core.agent import ReActAgent

from setup_llm import groq_llm
from note_engine import note_engine
from prompts import new_prompt, instruction_str, context
from pdf import canada_engine

load_dotenv()



population_path = os.path.join("data", "WorldPopulation2023.csv")
population_df = pd.read_csv(population_path)
population_query_engine = PandasQueryEngine(df=population_df, verbose=True)

population_query_engine.update_prompts({"pandas_prompt": new_prompt})

tools = [
    note_engine,
    QueryEngineTool(
        query_engine=population_query_engine, 
        metadata=ToolMetadata(
            name="population_data",
            description="This gives information at the world population and demographics",
        )
    ),
    QueryEngineTool(
        query_engine=canada_engine, 
        metadata=ToolMetadata(
            name="canada_data",
            description="This gives detailed information about canada the country",
        )
    ),
]

agent = ReActAgent.from_tools(tools, llm=groq_llm, verbose=True, context=context)


while (prompt := input("Enter a prompt (q to quit): ")) != "q":
    result = agent.query(prompt)
    print(result)