import sys
import time

from dotenv import load_dotenv
from langchain import hub
from langchain.agents import AgentExecutor, create_structured_chat_agent
from langchain.memory import ConversationSummaryMemory
from langchain_community.chat_models import ChatOpenAI
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI

from config import VERBOSE
from tools.gmail_rag_tool import search_gmail_rag_tool
from tools.gmail_tool import search_gmail_combined_tool
from tools.time_tool import time_tool
from tools.news_summarizer_tool import news_tool

load_dotenv()

# Define the tools that the agent can use
tools = [
    time_tool,
    search_gmail_combined_tool,
    news_tool
]

# Load the correct JSON Chat Prompt from the hub
prompt = hub.pull("hwchase17/structured-chat-agent")

# Initialize a ChatOpenAI model
llm = ChatOpenAI(model="gpt-4o")

# Create a Conversation Summary Memory
memory = ConversationSummaryMemory(llm=llm, memory_key="summary")

# Create a structured Chat Agent with Conversation Summary Memory
agent = create_structured_chat_agent(llm=llm, tools=tools, prompt=prompt)

agent_executor = AgentExecutor.from_agent_and_tools(
    agent=agent,
    tools=tools,
    verbose=VERBOSE,
    memory=memory,
    handle_parsing_errors=True,
)

initial_message = "You are an AI assistant that can provide helpful answers using available tools.\nIf you are unable to answer, you can use the following tools: Time and Wikipedia."
memory.chat_memory.add_message(SystemMessage(content=initial_message))

# Chat Loop to interact with the user
while True:
    user_input = input("User: ")
    if user_input.lower() == "exit":
        break

    memory.chat_memory.add_user_message(HumanMessage(content=user_input))

    # Show loading message
    sys.stdout.write("Bot is thinking...\r")
    sys.stdout.flush()

    # Call the agent
    try:
        response = agent_executor.invoke({"input": user_input})
        # Print the bot's response
        print("Bot:", response["output"])

        memory.chat_memory.add_ai_message(AIMessage(content=response["output"]))
    except Exception as e:
        print("Error:", str(e))

    # Clear loading message
    sys.stdout.write(" " * 20 + "\r")
    sys.stdout.flush()
