import sys
import time
from dotenv import load_dotenv
from langchain import hub
from langchain.agents import AgentExecutor, create_structured_chat_agent
from langchain.memory import ConversationBufferMemory
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI
from tools.time_tool import time_tool
from tools.wikipedia_tool import wikipedia_tool
from tools.gmail_tool import search_gmail_combined_tool
from tools.gmail_rag_tool import search_gmail_rag_tool
from config import VERBOSE

load_dotenv()

# Define the tools that the agent can use
tools = [
    time_tool,
    search_gmail_rag_tool,
    # wikipedia_tool, # TODO: Fix this tool
]

# Load the correct JSON Chat Prompt from the hub
prompt = hub.pull("hwchase17/structured-chat-agent")

# Initialize a ChatOpenAI model
llm = ChatOpenAI(model="gpt-4o")

# Create a structured Chat Agent with Conversation Buffer Memory
memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

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

    memory.chat_memory.add_message(HumanMessage(content=user_input))

    # Show loading message
    sys.stdout.write("Bot is thinking...\r")
    sys.stdout.flush()

    # Call the agent
    response = agent_executor.invoke({"input": user_input})

    # Clear loading message
    sys.stdout.write(" " * 20 + "\r")
    sys.stdout.flush()

    # Print the bot's response
    print("Bot:", response["output"])

    memory.chat_memory.add_message(AIMessage(content=response["output"]))
