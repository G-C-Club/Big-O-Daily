import requests
import json

# 🔑 کلید جدید را مستقیماً اینجا بین دو کوتیشن قرار بده
API_KEY = "AIzaSyDj90of2c3pxABcP69rr_PA1k6zjlYJRDc"

# 🌐 تنظیمات پروکسی (دقیقاً همان که برای اسکرپر جواب داد)
PROXIES = {
    "http": "http://127.0.0.1:2080",
    "https": "http://127.0.0.1:2080"
}

def test_gemini_direct():
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={API_KEY}"
    
    headers = {'Content-Type': 'application/json'}
    payload = {
        "contents": [{"parts": [{"text": "Say hello in Persian"}]}]
    }

    print(f"🚀 Testing API directly with key: {API_KEY[:10]}...")
    
    try:
        response = requests.post(url, headers=headers, json=payload, proxies=PROXIES, timeout=30)
        
        if response.status_code == 200:
            print("✅ SUCCESS! The API Key is working perfectly.")
            print("Response:", response.json()['candidates'][0]['content']['parts'][0]['text'])
        else:
            print(f"❌ FAILED! Status Code: {response.status_code}")
            print("Full Error Message from Google:")
            print(response.text)
            
    except Exception as e:
        print(f"📡 Connection Error (Proxy problem?): {e}")

if __name__ == "__main__":
    test_gemini_direct()
