from dotenv import load_dotenv
import os
import pandas as pd

from llama_index.experimental.query_engine import PandasQueryEngine
from llama_index.core.tools import QueryEngineTool, ToolMetadata
from llama_index.core.agent import ReActAgent

from setup_llm import groq_llm
from engines_factory.excel_note_engine import excel_note_engine
from prompts import new_prompt, instruction_str, context
from pdf import canada_engine

load_dotenv()

population_path = os.path.join("data", "WorldPopulation2023.csv")
population_df = pd.read_csv(population_path)
population_query_engine = PandasQueryEngine(df=population_df, verbose=True)

population_query_engine.update_prompts({"pandas_prompt": new_prompt})

tools = [
    excel_note_engine,
    QueryEngineTool(
        query_engine=population_query_engine,
        metadata=ToolMetadata(
            name="population_data",
            description="""This tool provides comprehensive insights into global population statistics and demographics.""",
        ),
    ),
    QueryEngineTool(
        query_engine=canada_engine,
        metadata=ToolMetadata(
            name="canada_data",
            description="""This tool offers in-depth information about Canada, covering a wide range of topics.""",
        ),
    ),
]

agent = ReActAgent.from_tools(tools, llm=groq_llm, verbose=True, context=context)

# Initialize history as a list of dictionaries
history = []


def add_to_history(prompt, response):
    # Add a new entry to the history
    history.append({"prompt": prompt, "response": response})
    # Limit history to the last 5 interactions
    if len(history) > 5:
        history.pop(0)


def get_relevant_history():
    # Optionally, filter or summarize history here
    return "\n".join(
        [
            f"Prompt: {entry['prompt']}\nResponse: {entry['response']}"
            for entry in history
        ]
    )


while (prompt := input("Enter a prompt (q to quit): ")) != "q":
    # Get relevant history
    relevant_history = get_relevant_history()
    # Query the agent with the current prompt and relevant history
    result = agent.query(
        f"Here is the relevant history:\n{relevant_history}\n\nNew prompt: {prompt}"
    )
    # Add the current interaction to history
    add_to_history(prompt, result)
    print(result)
