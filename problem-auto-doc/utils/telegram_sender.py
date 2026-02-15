import requests
import os

def check_telegram_connection():
    """Checks if the Telegram Bot Token and Channel ID are valid."""
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHANNEL_ID")
    url = f"https://api.telegram.org/bot{token}/getChat?chat_id={chat_id}"
    
    try:
        response = requests.get(url, timeout=5)
        return response.status_code == 200
    except:
        return False
        
def format_telegram_message(data, day_num, github_url):
    """
    Formats the problem data into a professional Telegram post template.
    """
    title = data.get('title', 'Unknown Problem')
    link = data.get('link', '#')
    header = data.get('header_info', {})
    
    # 1. Basic Info
    message = f"📅 **Day {day_num:04d}**\n"
    message += f"❓ **Problem:** [{title}]({link})\n\n"
    
    # 2. Details Section
    message += "```⚙️ Details\n"
    message += f"Time   : {header.get('time', 'N/A')}\n"
    message += f"Memory : {header.get('memory', 'N/A')}\n"
    message += "```\n"
    
    # 3. Tags Section (Formatted as Hashtags)
    if data.get('tags'):
        tags = " ".join([f"#{tag.replace(' ', '_').replace('*', '')}" for tag in data['tags']])
        message += f"```Tags\n{tags}\n```\n"
    
    # 4. Description
    message += f"```📖 Description\n{data.get('statement', '')[:500]}...\n```\n\n"
    
    # 5. Input/Output Specs
    message += f"```📥 Input Specification\n{data.get('input_spec', 'N/A')[:200]}...\n```\n"
    message += f"```📤 Output Specification\n{data.get('output_spec', 'N/A')[:200]}...\n```\n\n"
    
    # 6. Samples
    message += "🧪 **Example:**\n"
    for i, sample in enumerate(data.get('samples', [])[:2]):  # Limit to 2 samples for brevity
        message += f"```Input {i+1}:\n{sample['input']}```\n"
        message += f"```Output {i+1}:\n{sample['output']}```\n"
    
    # 7. Footer & Links
    clean_title = title.replace('/', '-').replace('\\', '-')
    problem_github_link = f"{github_url}/tree/main/problems/Day{day_num:04d}%20-%20{clean_title.replace(' ', '%20')}"
    
    message += f"\n🔗 [View on GitHub]({problem_github_link})\n"
    message += f"📂 [Full Repository]({github_url})\n"
    ID_Channle = os.getenv("TELEGRAM_BOT_TOKEN")
    message += f"📢 {ID_Channle}"
    
    return message

def send_to_telegram(message):
    """
    Sends the formatted message to the specified Telegram channel.
    """
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHANNEL_ID")
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    
    payload = {
        "chat_id": chat_id,
        "text": message,
        "parse_mode": "Markdown",
        "disable_web_page_preview": True
    }
    
    try:
        response = requests.post(url, json=payload)
        if response.status_code == 200:
            print("✅ Successfully posted to Telegram!")
        else:
            print(f"❌ Telegram Error: {response.text}")
    except Exception as e:
        print(f"📡 Connection failed to Telegram: {e}")
