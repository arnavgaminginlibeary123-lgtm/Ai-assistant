import os
import requests
import json
import re
from typing import List, Dict
from openai import OpenAI

# ========== CONFIGURATION ==========
# 1. Open your terminal/command prompt and run: pip install openai requests
# 2. Put your keys inside the quotes below:
OPENAI_API_KEY = "your-openai-api-key-here"
SERPER_API_KEY = "your-serper-api-key-here" 
WEATHER_API_KEY = "your-weather-api-key-here"

# Initialize OpenAI Client (Updated for OpenAI v1.0+)
client = OpenAI(api_key=OPENAI_API_KEY)

class InternetAIChatbot:
    def __init__(self):
        self.conversation_history = []
        self.max_history = 10
        
    def google_search(self, query: str) -> str:
        """Search Google using Serper API"""
        try:
            headers = {"X-API-KEY": SERPER_API_KEY, "Content-Type": "application/json"}
            data = {"q": query, "num": 5}
            response = requests.post("https://google.serper.dev/search", headers=headers, json=data)
            results = response.json()
            
            search_results = []
            for result in results.get("organic", []):
                search_results.append(f"• {result.get('title', '')}: {result.get('snippet', '')}")
            
            return "\n".join(search_results[:3]) if search_results else "No search results found."
        except Exception as e:
            return f"Search error: {str(e)}"

    def get_weather(self, city: str) -> str:
        """Get weather using WeatherAPI"""
        try:
            url = "http://api.weatherapi.com/v1/current.json"
            params = {"key": WEATHER_API_KEY, "q": city}
            response = requests.get(url, params=params)
            data = response.json()
            
            if "error" in data:
                return f"Could not find weather for '{city}'."

            current = data["current"]
            location = data["location"]
            return (f"Weather in {location['name']}: {current['temp_c']}°C, {current['condition']['text']}.")
        except Exception as e:
            return f"Weather error: {str(e)}"

    def detect_intent(self, user_input: str) -> str:
        """Detect if user wants weather, search, or just chat"""
        user_input_lower = user_input.lower()
        if any(word in user_input_lower for word in ["weather", "temperature"]):
            return "weather"
        elif any(word in user_input_lower for word in ["search", "google", "find"]):
            return "search"
        return "chat"

    def get_openai_response(self, user_input: str, context: str = "") -> str:
        """Get response from OpenAI GPT with memory"""
        try:
            messages = [{"role": "system", "content": f"You are ArnavBot. Context: {context}"}]
            
            # Add history
            for chat in self.conversation_history:
                messages.append({"role": "user", "content": chat["user"]})
                messages.append({"role": "assistant", "content": chat["bot"]})

            messages.append({"role": "user", "content": user_input})
            
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=messages,
                max_tokens=500
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            return f"OpenAI Error: {str(e)}"

    def process_message(self, user_input: str) -> str:
        """Logic to decide which API to call"""
        intent = self.detect_intent(user_input)
        context = ""
        
        if intent == "weather":
            # Extract the last word as the city
            city = user_input.split()[-1].strip("?.!")
            context = self.get_weather(city)
        elif intent == "search":
            query = user_input.replace("search", "").replace("google", "").strip()
            context = self.google_search(query)
            
        response = self.get_openai_response(user_input, context)
        
        # Save to memory
        self.conversation_history.append({"user": user_input, "bot": response})
        if len(self.conversation_history) > self.max_history:
            self.conversation_history.pop(0)
            
        return response

    def chat(self):
        """The main interaction loop"""
        print("\n🚀 ArnavBot Active! (Type 'quit' to stop)")
        while True:
            user_input = input("You: ").strip()
            if user_input.lower() in ['quit', 'exit']:
                break
            if not user_input:
                continue
            
            print("🤖 ArnavBot: ", end="", flush=True)
            print(self.process_message(user_input))

if __name__ == "__main__":
    chatbot = InternetAIChatbot()
    chatbot.chat()
        "Main message processing logic"
        intent = self.detect_intent(user_input)
        context = ""
        
        if intent == "weather":
            # Simple logic to extract city (last word usually)
            words = user_input.split()
            city = words[-1].strip("?!.") if len(words) > 1 else "Delhi"
            context = self.get_weather(city)
            response = self.get_openai_response(user_input, context)
            
        elif intent == "search":
            query = re.sub(r'(search|google|find|for)', '', user_input, flags=re.IGNORECASE).strip()
            context = self.google_search(query)
            response = self.get_openai_response(user_input, context)
            
        else:
            response = self.get_openai_response(user_input)
        
        # Update conversation history
        self.conversation_history.append({"user": user_input, "bot": response})
        if len(self.conversation_history) > self.max_history:
            self.conversation_history.pop(0)
            
        return response

    def chat(self):
        """Main chat loop"""
        print("\n🤖 ArnavBot - Advanced AI Chatbot")
        print("Made by Arnav Srivastava")
        print("=" * 50)
        print("Commands: 'weather [city]', 'search [query]', 'quit'")
        print("=" * 50)
        
        while True:
            user_input = input("You: ").strip()
            
            if user_input.lower() in ['quit', 'exit', 'bye']:
                print("👋 ArnavBot: Goodbye! Made by Arnav Srivastava 🚀")
                break
            
            if not user_input:
                continue
                
            print("🤖 ArnavBot: ", end="", flush=True)
            response = self.process_message(user_input)
            print(response)

# ========== MAIN EXECUTION ==========
if __name__ == "__main__":
    chatbot = InternetAIChatbot()
    print("🚀 Starting ArnavBot - Full Internet AI Chatbot!")
    chatbot.chat()
