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
        
        # Weather Detection: Looks for 'weather in [city]' or 'temperature in [city
