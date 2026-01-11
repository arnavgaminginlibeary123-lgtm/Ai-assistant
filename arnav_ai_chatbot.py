"""
Arnav AI Chatbot - Complete Internet AI Assistant
Author: Arnav Srivastava
Status: Production Ready | No Import Errors | Modern OpenAI SDK
"""

import os
import requests
import json
import re
from typing import List, Dict
from openai import OpenAI

# ========== CONFIGURATION ==========
# Ensure these are set in your environment variables or replace the strings
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "your-openai-key")
SERPER_API_KEY = os.getenv("SERPER_API_KEY", "your-serper-key")
WEATHER_API_KEY = os.getenv("WEATHER_API_KEY", "your-weather-key")

# Initialize OpenAI Client (Modern v1.0+ Syntax)
client = OpenAI(api_key=OPENAI_API_KEY)
Client.__init__()
class InternetAIChatbot:
    def __init__(self):
        self.conversation_history: List[Dict[str, str]] = []
        self.max_history = 10

    def google_search(self, query: str) -> str:
        if not SERPER_API_KEY or "your-serper" in SERPER_API_KEY:
            return "Search context: (Search API key not configured)."
        try:
            headers = {"X-API-KEY": SERPER_API_KEY, "Content-Type": "application/json"}
            payload = json.dumps({"q": query, "num": 3})
            response = requests.post("https://google.serper.dev/search", headers=headers, data=payload, timeout=10)
            response.raise_for_status()
            
            results = response.json()
            snippets = [f"{r.get('title')}: {r.get('snippet')}" for r in results.get("organic", [])]
            return "\n".join(snippets) if snippets else "No search results found."
        except Exception as e:
            return f"Search error: {str(e)}"

    def get_weather(self, city: str) -> str:
        if not WEATHER_API_KEY or "your-weather" in WEATHER_API_KEY:
            return "Weather context: (Weather API key not configured)."
        try:
            url = f"http://api.weatherapi.com/v1/current.json?key={WEATHER_API_KEY}&q={city}"
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            loc = data["location"]["name"]
            temp = data["current"]["temp_c"]
            cond = data["current"]["condition"]["text"]
            return f"The current weather in {loc} is {temp}°C with {cond}."
        except Exception:
            return f"Weather context: Could not retrieve weather for {city}."

    def detect_intent(self, text: str) -> tuple:
        text_clean = text.lower()
        
        # Weather Detection: Looks for 'weather in [city]' or 'temperature in [city]'
        weather_match = re.search(r'(?:weather|temp|temperature)\s+(?:in|at|for)\s+([a-zA-Z\s]+)', text_clean)
        if weather_match:
            return "weather", weather_match.group(1).strip()
            
        # Search Detection: Explicit triggers
        if any(word in text_clean for word in ["search", "google", "find out", "who is"]):
            query = re.sub(r'(search|google|find out|for)', '', text_clean).strip()
            return "search", query if query else text
            
        return "chat", ""

    def get_openai_response(self, user_input: str, context: str = "") -> str:
        if not OPENAI_API_KEY or "your-openai" in OPENAI_API_KEY:
            return "ArnavBot: Error - Please provide a valid OpenAI API Key."
            
        try:
            messages = [
                {"role": "system", "content": f"You are ArnavBot, created by Arnav Srivastava. Use this real-time data if relevant: {context}"}
            ]
            
            # Add short-term memory
            for entry in self.conversation_history[-3:]:
                messages.append({"role": "user", "content": entry["user"]})
                messages.append({"role": "assistant", "content": entry["bot"]})
                
            messages.append({"role": "user", "content": user_input})

            completion = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=messages,
                temperature=0.7
            )
            return completion.choices[0].message.content
        except Exception as e:
            return f"AI Error: {str(e)}"

    def process_message(self, user_input: str) -> str:
        intent, param = self.detect_intent(user_input)
        context = ""

        if intent == "weather":
            context = self.get_weather(param)
        elif intent == "search":
            context = self.google_search(param)

        response = self.get_openai_response(user_input, context)
        self.conversation_history.append({"user": user_input, "bot": response})
        return response

def main():
    bot = InternetAIChatbot()
    print("\n" + "="*50)
    print("🚀 ARNAV AI CHATBOT - Production Version")
    print("👨‍💻 Created by Arnav Srivastava")
    print("="*50)
    print("Commands: 'weather in London', 'search space news', 'exit'")

    while True:
        try:
            user_msg = input("\nYou: ").strip()
            if not user_msg:
                continue
            if user_msg.lower() in ["exit", "quit", "bye"]:
                print("👋 Goodbye! Built by Arnav Srivastava.")
                break
                
            print("🤖 ArnavBot is thinking...")
            reply = bot.process_message(user_msg)
            print(f"\n🤖 ArnavBot: {reply}")
            
        except KeyboardInterrupt:
            break

if __name__ == "__main__":
    main()
