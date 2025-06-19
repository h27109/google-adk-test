from google.adk.agents import Agent

root_agent = Agent(
    name = "simple_agent",
    model = "gemini-2.0-flash-exp",
    description = ("A simple agent that can answer questions"),
    instruction = ("You are a helpful assistant that can answer questions"),
    tools = []
)