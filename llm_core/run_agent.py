from .agent_builder import build_agent

# Initialize history as a list of dictionaries
history = []
agent = build_agent()


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
