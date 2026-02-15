import requests
import json
import time
import os
from dotenv import load_dotenv

load_dotenv()

class AITranslator:
    def __init__(self):
        """
        Initializes the translator with retry logic and proxy support.
        """
        self.api_key = os.getenv("GEMINI_API_KEY") 
        if not self.api_key:
            raise ValueError("❌ Error: GEMINI_API_KEY is missing in .env")

        self.proxy_url = "http://127.0.0.1:2080"
        self.proxies = {"http": self.proxy_url, "https": self.proxy_url}

        # Confirmed stable model name
        self.model_name = "gemini-2.5-flash" 
        self.api_url = f"https://generativelanguage.googleapis.com/v1beta/models/{self.model_name}:generateContent?key={self.api_key}"

    def translate_sections(self, data):
        """
        Translates descriptive sections only. Skips tags as requested.
        """
        translated_data = data.copy()
        
        # Sections that require AI translation
        sections_to_translate = {
            "title": "Problem Title",
            "statement": "Problem Description",
            "input_spec": "Input Specifications",
            "output_spec": "Output Specifications",
            "note": "Explanatory Note"
        }

        print(f"   -> 🤖 Translating descriptive sections...")

        for key, context in sections_to_translate.items():
            text = translated_data.get(key, "")
            
            if text and len(text.strip()) > 0:
                success = False
                for attempt in range(1, 4):
                    try:
                        translated_text = self._ask_ai(text, context)
                        # Wrap in RTL tags for Persian alignment
                        translated_data[key] = translated_text
                        print(f"      ✓ Translated: {key}")
                        success = True
                        break 
                    except Exception as e:
                        print(f"      ⚠️ Attempt {attempt} failed for {key}: {e}")
                        if attempt < 3:
                            time.sleep(5) 
                
                if not success:
                    raise Exception(f"Critical section translation failed: {key}")
                
                time.sleep(1)

        # Tags remain unchanged (English)
        return translated_data

    def _ask_ai(self, text, context_type):
        """
        Core request logic for Gemini API.
        """
        prompt = f"""
        Act as a professional competitive programming coach. 
        Translate the following "{context_type}" from English into Persian (Farsi).
        
        STRICT RULES:
        1. Keep all LaTeX formulas ($...$ or $$...$$) UNCHANGED.
        2. Keep all code variables (` `) UNCHANGED.
        3. Use professional Persian terminology.
        4. Provide ONLY the translated text.

        Content:
        {text}
        """
        
        headers = {'Content-Type': 'application/json'}
        payload = {"contents": [{"parts": [{"text": prompt}]}]}

        response = requests.post(
            self.api_url, 
            headers=headers, 
            json=payload, 
            proxies=self.proxies, 
            timeout=90
        )
        
        if response.status_code == 200:
            res_json = response.json()
            if 'candidates' in res_json and res_json['candidates']:
                return res_json['candidates'][0]['content']['parts'][0]['text'].strip()
            raise Exception("Empty response from AI.")
        else:
            raise Exception(f"API Error {response.status_code}")
