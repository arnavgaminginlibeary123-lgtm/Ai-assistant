"""
Arnav AI Chatbot - Enhanced Internet AI Assistant
Made by Arnav Srivastava
Updated: Modern OpenAI API v1.0+, improved regex, and error handling.
"""

import os
import requests
import json
import re
from datetime import datetime
from typing import List, Dict
from openai import OpenAI

# ========== CONFIGURATION ==========
# Use environment variables for security
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "your-openai-key")
SERPER_API_KEY = os.getenv("SERPER_API_KEY", "your-serper-key")
WEATHER_API_KEY = os.getenv("WEATHER_API_KEY", "your-weather-key")

# Initialize OpenAI Client
client = OpenAI(api_key=OPENAI_API_KEY)

class InternetAIChatbot:
    def __init__(self):
        self.conversation_history = []
        self.max_history = 10

    def google_search(self, query: str) -> str:
        if not SERPER_API_KEY or "your-serper-key" in SERPER_API_KEY:
            return "Error: Missing Serper API Key."
        try:
            headers = {
                "X-API-KEY": SERPER_API_KEY,
                "Content-Type": "application/json"
            }
            data = {"q": query, "num": 3}
            response = requests.post(
                "https://google.serper.dev/search",
                headers=headers,
                json=data,
                timeout=10
            )
            response.raise_for_status()
            results = response.json()
            
            search_results = []
            for result in results.get("organic", [])[:3]:
                title = result.get('title', 'No title')
                snippet = result.get('snippet', '')
                search_results.append(f"**{title}**: {snippet}")
            
            return "\n".join(search_results) if search_results else "No relevant search results found."
        except Exception as e:
            return f"Search error: {str(e)}"

    def get_weather(self, city: str = "Delhi") -> str:
        if not WEATHER_API_KEY or "your-weather-key" in WEATHER_API_KEY:
            return "Error: Missing Weather API Key."
        try:
            url = f"http://api.weatherapi.com/v1/current.json"
            params = {"key": WEATHER_API_KEY, "q": city}
            response = requests.get(url, params=params, timeout=10)
            data = response.json()
            
            if "error" in data:
                return f"Could not find weather for '{city}'."
                
            loc = data["location"]
            cur = data["current"]
            return f"Weather in {loc['name']}, {loc['country']}: {cur['temp_c']}°C, {cur['condition']['text']}. Feels like {cur['feelslike_c']}°C."
        except Exception as e:
            return "Weather service currently unavailable."

    def detect_intent(self, user_input: str) -> tuple:
        text = user_input.lower()
        
        # Weather intent: Extract city after 'in' or 'at'
        if any(word in text for word in ["weather", "temperature", "temp"]):
            city_match = re.search(r'(?:in|at)\s+([a-zA-Z\s]+)', text)
            city = city_match.group(1).strip() if city_match else "Delhi"
            return "weather", city
            
        # Search intent
        elif any(word in text for word in ["search", "google", "find", "who is", "what is"]):
            query = re.sub(r'(search|google|find|for)', '', text, flags=re.IGNORECASE).strip()
            return "search", query or text
            
        return "chat", ""

    def get_openai_response(self, user_input: str, context: str = "") -> str:
        if not OPENAI_API_KEY or "your-openai-key" in OPENAI_API_KEY:
            return "❌ API Key Error: Please set your OPENAI_API_KEY."
        
        try:
            messages = [
                {
                    "role": "system", 
                    "content": f"You are ArnavBot, a high-performance AI made by Arnav Srivastava. Use this context if helpful: {context}"
                }
            ]
            
            # Add conversation history for memory
            for turn in self.conversation_history[-5:]:
                messages.append({"role": "user", "content": turn["user"]})
                messages.append({"role": "assistant", "content": turn["bot"]})
            
            messages.append({"role": "user", "content": user_input})

            response = client.chat.completions.create(
                model="gpt-3.5-turbo", # Or gpt-4-turbo
                messages=messages,
                max_tokens=500,
                temperature=0.7
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            return f"🤖 AI Error: {str(e)}"

    def process_message(self, user_input: str) -> str:
        intent, param = self.detect_intent(user_input)
        context = ""

        if intent == "weather":
            context = self.get_weather(param)
        elif intent == "search":
            context = self.google_search(param)

        response = self.get_openai_response(user_input, context)
        
        # Save to history
        self.conversation_history.append({"user": user_input, "bot": response})
        if len(self.conversation_history) > self.max_history:
            self.conversation_history.pop(0)
            
        return response

    def chat(self):
        print("\n" + "="*50)
        print("🤖 Arnav AI Chatbot - Made by Arnav Srivastava")
        print("="*50)
        print("Try: 'Weather in London' or 'Search for space black holes'")
        print("Type 'quit' to exit.")

        while True:
            user_input = input("\nYou: ").strip()
            if user_input.lower() in ['quit', 'exit', 'bye']:
                print("👋 Goodbye! Project by Arnav Srivastava.")
                break
            if not user_input:
                continue

            print("🤖 ArnavBot: ", end="", flush=True)
            response = self.process_message(user_input)
            print(response)

# ========== MAIN EXECUTION ==========
if __name__ == "__main__":
    chatbot = InternetAIChatbot()
    chatbot.chat()
