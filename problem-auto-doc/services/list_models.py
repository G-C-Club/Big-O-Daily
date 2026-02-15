import requests
import os
import json
from dotenv import load_dotenv

# Load your API key from .env
load_dotenv()

def get_available_models():
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("❌ Error: GEMINI_API_KEY not found in .env file.")
        return

    # Using your working proxy
    proxy_url = "http://127.0.0.1:2080"
    proxies = {
        "http": proxy_url,
        "https": proxy_url
    }

    # Google API endpoint to list models
    url = f"https://generativelanguage.googleapis.com/v1beta/models?key={api_key}"

    print(f"🔍 Fetching allowed models from Google...")
    print(f"🌍 Via Proxy: {proxy_url}")
    print("-" * 50)

    try:
        response = requests.get(url, proxies=proxies, timeout=30)
        
        if response.status_code == 200:
            models_data = response.json()
            models = models_data.get('models', [])
            
            print(f"✅ Success! Found {len(models)} models total.\n")
            print(f"{'Model Name':<40} | {'Generation Support'}")
            print("-" * 65)
            
            for m in models:
                # Check if the model supports content generation (important for our tool)
                can_generate = "generateContent" in m.get('supportedGenerationMethods', [])
                gen_status = "✅ YES" if can_generate else "❌ NO"
                
                # We only care about models starting with 'models/'
                print(f"{m['name']:<40} | {gen_status}")
                
            print("-" * 65)
            print("\n💡 Tip: Use the full name (e.g., models/gemini-1.5-flash) in your script.")
            
        else:
            print(f"❌ Failed! Status Code: {response.status_code}")
            print("Response:", response.text)

    except Exception as e:
        print(f"📡 Connection Error: {e}")

if __name__ == "__main__":
    get_available_models()
