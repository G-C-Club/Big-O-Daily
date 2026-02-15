import requests
import os
from dotenv import load_dotenv

# Load .env explicitly
load_dotenv(os.path.join(os.path.dirname(os.getcwd()), '.env')) # Adjusted path if you are inside 'services' folder

api_key = os.getenv("GEMINI_API_KEY")
proxies = {
    "http": "http://127.0.0.1:2080",
    "https": "http://127.0.0.1:2080"
}

url = f"https://generativelanguage.googleapis.com/v1beta/models?key={api_key}"

print(f"🔍 Checking available models...")
print(f"🌍 Proxy: {proxies['http']}")

try:
    # Increased timeout to 120 seconds
    response = requests.get(url, proxies=proxies, timeout=120)
    
    if response.status_code == 200:
        data = response.json()
        print("\n✅ Success! Available Models:")
        for model in data.get('models', []):
            if "generateContent" in model.get('supportedGenerationMethods', []):
                print(f"   👉 {model['name']}")
    else:
        print(f"\n❌ HTTP Error {response.status_code}: {response.text}")

except Exception as e:
    print(f"\n❌ Connection Failed: {e}")
