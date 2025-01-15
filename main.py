from dotenv import load_dotenv
from langchain import hub
from langchain.agents import AgentExecutor, create_structured_chat_agent
from langchain.memory import ConversationBufferMemory
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI
from tools.time_tool import time_tool
from tools.wikipedia_tool import wikipedia_tool
from tools.gmail_live_tool import search_gmail_live_tool
from tools.gmail_rag_tool import search_gmail_rag_tool

load_dotenv()

# Define the tools that the agent can use
tools = [
    time_tool,
    search_gmail_rag_tool,
    # search_gmail_live_tool,
    # wikipedia_tool, # TODO: Fix this tool
]

# Load the correct JSON Chat Prompt from the hub
prompt = hub.pull("hwchase17/structured-chat-agent")

# Initialize a ChatOpenAI model
llm = ChatOpenAI(model="gpt-4o")

# Create a structured Chat Agent with Conversation Buffer Memory
# ConversationBufferMemory stores the conversation history, allowing the agent to maintain context across interactions
memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

# create_structured_chat_agent initializes a chat agent designed to interact using a structured prompt and tools
# It combines the language model (llm), tools, and prompt to create an interactive agent
agent = create_structured_chat_agent(llm=llm, tools=tools, prompt=prompt)

# AgentExecutor is responsible for managing the interaction between the user input, the agent, and the tools
# It also handles memory to ensure context is maintained throughout the conversation
agent_executor = AgentExecutor.from_agent_and_tools(
    agent=agent,
    tools=tools,
    verbose=True,
    memory=memory,
    handle_parsing_errors=True,
)

# Initial system message to set the context for the chat
initial_message = "You are an AI assistant that can provide helpful answers using available tools.\nIf you are unable to answer, you can use the following tools: Time and Wikipedia."
memory.chat_memory.add_message(SystemMessage(content=initial_message))

# Chat Loop to interact with the user
while True:
    user_input = input("User: ")
    if user_input.lower() == "exit":
        break

    # Add the user's message to the conversation memory
    memory.chat_memory.add_message(HumanMessage(content=user_input))

    # Invoke the agent with the user input and the current chat history
    response = agent_executor.invoke({"input": user_input})
    print("Bot:", response["output"])

    # Add the agent's response to the conversation memory
    memory.chat_memory.add_message(AIMessage(content=response["output"]))
