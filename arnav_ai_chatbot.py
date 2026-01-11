"""
Advanced AI Chatbot with Multiple Internet APIs
Made by Arnav Srivastava
This chatbot integrates OpenAI, Google Search (Serper), Weather API, and more!
"""

import os
import openai
import requests
import json
from datetime import datetime
import re
from typing import List, Dict

# ========== CONFIGURATION ==========
# Get your API keys from:
# OpenAI: https://platform.openai.com/
# Serper (Google Search): https://serper.dev/
# WeatherAPI: https://www.weatherapi.com/
OPENAI_API_KEY = "your-openai-api-key-here"
SERPER_API_KEY = "your-serper-api-key-here" 
WEATHER_API_KEY = "your-weather-api-key-here"

# Initialize OpenAI
openai.api_key = OPENAI_API_KEY

class InternetAIChatbot:
    def __init__(self):
        self.conversation_history = []
        self.max_history = 10
        
    def google_search(self, query: str) -> str:
        """Search Google using Serper API"""
        try:
            headers = {
                "X-API-KEY": SERPER_API_KEY,
                "Content-Type": "application/json"
            }
            data = {
                "q": query,
                "num": 5
            }
            response = requests.post(
                "https://google.serper.dev/search",
                headers=headers,
                json=data
            )
            results = response.json()
            
            search_results = []
            for result in results.get("organic", []):
                search_results.append(f"• {result.get('title', '')}: {result.get('snippet', '')}")
            
            return 
".join(search_results[:3]) if search_results else "No search results found.
        except Exception as e:
            return f"Search error: {str(e)}"

    def get_weather(self, city: str) -> str:
        """Get weather using WeatherAPI"""
        try:
            url = f"http://api.weatherapi.com/v1/current.json"
            params = {
                "key": WEATHER_API_KEY,
                "q": city
            }
            response = requests.get(url, params=params)
            data = response.json()
            
            current = data["current"]
            location = data["location"]
            return (f"Weather in {location['name']}, {location['country']}: "
                   f"{current['temp_c']}°C, {current['condition']['text']}, "
                   f"Feels like {current['feelslike_c']}°C")
        except Exception as e:
            return f"Weather error for {city}: {str(e)}"

    def detect_intent(self, user_input: str) -> str:
        """Detect user intent"""
        user_input_lower = user_input.lower()
        
        if any(word in user_input_lower for word in ["weather", "temperature"]):
            city_match = re.search(r'(?:ins+)?([a-zA-Zs]+?)(?:?|!|$)', user_input_lower)
            return "weather" if city_match else "general"
        elif any(word in user_input_lower for word in ["search", "google", "find"]):
            return "search"
        return "chat"

    def get_openai_response(self, user_input: str, context: str = "") -> str:
        """Get response from OpenAI GPT"""
        try:
            # Build messages with conversation history
            messages = [
                {
                    "role": "system",
                    "content": (
                        "You are ArnavBot, an advanced AI assistant made by Arnav Srivastava. "
                        "You have access to real-time internet data. Be helpful, witty, and informative. "
                        f"Context: {context}"
                    )
                },
                {"role": "user", "content": user_input}
            ]
            
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=messages,
                max_tokens=500,
                temperature=0.7
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            return f"Sorry, AI processing error: {str(e)}"

    def process_message(self, user_input: str) -> str:
        """Main message processing logic"""
        intent = self.detect_intent(user_input)
        context = ""
        
        if intent == "weather":
            # Extract city name
            city_match = re.search(r'(?:ins+)?([a-zA-Zs]+?)(?:?|!|$)', user_input.lower())
            city = city_match.group(1).strip() if city_match else "Delhi"
            context = self.get_weather(city)
            response = self.get_openai_response(
                user_input, 
                f"Weather data: {context}"
            )
            
        elif intent == "search":
            query = re.sub(r'(?:search|google|find).*?(fors*)?', '', user_input, flags=re.IGNORECASE).strip()
            context = self.google_search(query)
            response = self.get_openai_response(
                user_input,
                f"Search results: {context}"
            )
            
        else:
            response = self.get_openai_response(user_input)
        
        # Update conversation history
        self.conversation_history.append({"user": user_input, "bot": response})
        if len(self.conversation_history) > self.max_history:
            self.conversation_history.pop(0)
            
        return response

    def chat(self):
        """Main chat loop"""
        print("🤖 ArnavBot - Advanced AI Chatbot")
        print("Made by Arnav Srivastava")
        print("=" * 50)
        print("Commands: 'weather [city]', 'search [query]', 'quit'")
        print("=" * 50)
        
        while True:
            user_input = input("
You: ").strip()
            
            if user_input.lower() in ['quit', 'exit', 'bye']:
                print("👋 ArnavBot: Goodbye! Made by Arnav Srivastava 🚀")
                break
            
            if not user_input:
                continue
                
            print("🤖 ArnavBot: ", end="", flush=True)
            response = self.process_message(user_input)
            print(response)

# ========== ADDITIONAL FEATURES ==========
def save_conversation(history: List[Dict]):
    """Save conversation to file"""
    with open("chat_history.json", "w") as f:
        json.dump(history, f, indent=2)

def load_conversation() -> List[Dict]:
    """Load conversation from file"""
    try:
        with open("chat_history.json", "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return []

# ========== MAIN EXECUTION ==========
if __name__ == "__main__":
    # Load previous conversation
    chatbot = InternetAIChatbot()
    
    print("🚀 Starting ArnavBot - Full Internet AI Chatbot!")
    print("📱 Features: OpenAI GPT + Google Search + Weather API")
    print("👨‍💻 Made by Arnav Srivastava")
    print("-" * 60)
    
    chatbot.chat()
