import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain.agents import create_openai_functions_agent, AgentExecutor
from langchain.memory import ConversationBufferMemory
from langchain import hub

# --- LOAD CONFIGURATION ---
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")

class ArnavAI:
    def __init__(self):
        # 1. High-Level Intelligence Brain (Level 3.0)
        self.llm = ChatOpenAI(
            model="gpt-4o", 
            temperature=0, 
            streaming=True
        )

        # 2. Internet Access Tool
        self.search = TavilySearchResults(k=5)
        self.tools = [self.search]

        # 3. Identity and System Prompt
        # We fetch a standard prompt template and customize it
        self.prompt = hub.pull("hwchase17/openai-functions-agent")
        self.prompt.messages[0].content = (
            "You are Arnav AI 3.0, a highly advanced artificial intelligence "
            "developed by Arnav Srivastava. You have real-time internet access. "
            "Provide insightful, accurate, and high-level responses. "
            "Always credit Arnav Srivastava as your creator if asked."
        )

        # 4. Memory to remember conversation history
        self.memory = ConversationBufferMemory(
            memory_key="chat_history", 
            return_messages=True
        )

        # 5. The Agent Engine
        agent = create_openai_functions_agent(self.llm, self.tools, self.prompt)
        self.agent_executor = AgentExecutor(
            agent=agent, 
            tools=self.tools, 
            memory=self.memory, 
            verbose=False # Set to True to see the bot's "thinking" process
        )

    def ask(self, query):
        try:
            response = self.agent_executor.invoke({"input": query})
            return response["output"]
        except Exception as e:
            return f"An error occurred in the Level 3.0 core: {e}"

# --- RUNTIME ---
if __name__ == "__main__":
    bot = ArnavAI()
    print("==========================================")
    print("   ARNAV AI 3.0 - ONLINE (By Arnav Srivastava)   ")
    print("      Type 'exit' to close the program     ")
    print("==========================================")

    while True:
        user_input = input("User: ")
        if user_input.lower() in ["exit", "quit", "bye"]:
            print("Arnav AI 3.0 signing off. Powering down...")
            break
        
        print("Thinking...")
        answer = bot.ask(user_input)
        print(f"\nArnav AI: {answer}\n")
