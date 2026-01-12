import os
from langchain_openai import ChatOpenAI
from langchain_community.tools.tavily_search import TavilyAnswerRetriever
from langchain.agents import initialize_agent, AgentType
from langchain.memory import ConversationBufferMemory
from langchain.prompts import MessagesPlaceholder

# 1. SETUP CREDENTIALS
os.environ["OPENAI_API_KEY"] = "your_openai_key_here"
os.environ["TAVILY_API_KEY"] = "your_tavily_key_here"

def build_arnav_ai():
    # 2. THE BRAIN (Level 3.0 Intelligence)
    # Using gpt-4o for high-level reasoning and real-time processing
    llm = ChatOpenAI(model="gpt-4o", temperature=0.7)

    # 3. THE INTERNET ACCESS (Search Tool)
    search_tool = TavilyAnswerRetriever(k=3) # Fetches top 3 web results
    tools = [search_tool]

    # 4. CONVERSATIONAL MEMORY
    memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

    # 5. IDENTITY SETTINGS (The "Arnav Srivastava" Touch)
    system_message = {
        "role": "system",
        "content": (
            "You are an elite AI Chatbot created by Arnav Srivastava. "
            "You have high-level 3.0 intelligence and full access to the internet. "
            "Your goal is to provide deep, accurate, and real-time information. "
            "Always maintain a professional yet innovative tone, reflecting Arnav's vision."
        )
    }

    # 6. INITIALIZE AGENT
    agent = initialize_agent(
        tools, 
        llm, 
        agent=AgentType.CHAT_CONVERSATIONAL_REACT_DESCRIPTION, 
        verbose=True, 
        memory=memory,
        agent_kwargs={
            "system_message": system_message["content"],
            "extra_prompt_messages": [MessagesPlaceholder(variable_name="chat_history")]
        }
    )
    
    return agent

# 7. RUN THE BOT
if __name__ == "__main__":
    print("--- Arnav Srivastava's AI 3.0 is Online ---")
    bot = build_arnav_ai()
    
    while True:
        user_input = input("You: ")
        if user_input.lower() in ["exit", "quit"]:
            break
            
        response = bot.run(input=user_input)
        print(f"\nAI (Arnav Bot): {response}\n")
