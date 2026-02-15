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
    Formats the problem data into a professional Telegram post template using HTML.
    """
    title = data.get('title', 'Unknown Problem')
    link = data.get('link', '#')
    header = data.get('header_info', {})
    channel_id = os.getenv("TELEGRAM_CHANNEL_ID", "@Big_O_Daily")
    
    # 1. Basic Info (HTML Style)
    message = f"📅 <b>Day {day_num:04d}</b>\n"
    message += f"❓ <b>Problem:</b> <a href='{link}'>{title}</a>\n\n"
    
    if 'author' in data:
        author_info = data['author']
        message += f"✍️ <b>Author:</b> <a href='{author_info['github']}'>{author_info['name']}</a>"
        if author_info.get('telegram'):
            tg_link = f"https://t.me/{author_info['telegram']}"
            message += f" | <a href='{tg_link}'>📱 Telegram</a>"
        message += "\n\n"

    # 2. Details Section (Fixed width with <pre>)
    message += "<pre>⚙️ Details\n"
    message += f"Time   : {header.get('time', 'N/A')}\n"
    message += f"Memory : {header.get('memory', 'N/A')}\n"
    message += "</pre>\n"
    
    # 3. Tags Section
    if data.get('tags'):
        tags = " ".join([f"#{tag.replace(' ', '_').replace('*', '')}" for tag in data['tags']])
        message += f"<pre>Tags: {tags}</pre>\n\n"
    
    # 4. Description
    message += f"<b>📖 Description</b>\n{data.get('statement', '')[:500]}...\n\n"

    if data.get('input_spec'):
        message += f"<b>📥 Input Specification</b>\n{data.get('input_spec')}\n\n"
        
    if data.get('output_spec'):
        message += f"<b>📤 Output Specification</b>\n{data.get('output_spec')}\n\n"
        
    # 5. Samples
    message += "🧪 <b>Example:</b>\n"
    for i, sample in enumerate(data.get('samples', [])[:2]):
        message += f"<pre>Input {i+1}:\n{sample['input']}\n\nOutput {i+1}:\n{sample['output']}</pre>\n"

    # 6. Footer & Links
    clean_title = title.replace('/', '-').replace('\\', '-')
    problem_github_link = f"{github_url}/tree/main/problems/Day{day_num:04d}%20-%20{clean_title.replace(' ', '%20')}"
    
    message += f"\n🔗 <a href='{problem_github_link}'>View on GitHub</a>"
    message += f"\n📂 <a href='{github_url}'>Full Repository</a>"
    
    # 7. Your Custom Text
    message += "\n💡 <b>Share your ideas for solving this problem in the comments!</b>\n"

    # 8. Channel Link
    message += f"\n\n🧠 <b>Join us:</b> {channel_id}"
    return message

def send_to_telegram(message):
    """
    Sends the formatted message to the specified Telegram channel using HTML parse mode.
    """
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHANNEL_ID")
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    
    payload = {
        "chat_id": chat_id,
        "text": message,
        "parse_mode": "HTML", # Changed from Markdown to HTML to avoid parsing errors
        "disable_web_page_preview": True
    }
    
    try:
        response = requests.post(url, json=payload)
        if response.status_code == 200:
            print("✅ Successfully posted to Telegram!")
            return True
        else:
            print(f"❌ Telegram Error: {response.text}")
            return False
    except Exception as e:
        print(f"📡 Connection failed to Telegram: {e}")
        return False
