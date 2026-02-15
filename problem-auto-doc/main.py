import os
import json
from scrapers.codeforces import CodeforcesScraper
from scrapers.leetcode import LeetCodeScraper
from services.ai_translator import AITranslator
from utils.file_manager import generate_english_markdown, generate_persian_markdown, get_next_day_number
from utils.telegram_sender import format_telegram_message, send_to_telegram, check_telegram_connection
from utils.git_manager import check_git_connection, git_commit_and_push
from utils.sync_manager import update_database, sync_main_readme

def get_author_info():
    """Handles user selection and management from the data/users.json."""
    bot_folder = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(bot_folder, "data")
    users_path = os.path.join(data_dir, "users.json")
    
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)

    users = {}
    if os.path.exists(users_path):
        with open(users_path, "r", encoding="utf-8") as f:
            try:
                users = json.load(f)
            except json.JSONDecodeError:
                users = {}

    print("\n--- 👥 Select User ---")
    for uid, info in users.items():
        print(f"[{uid}] {info['name']}")
    print("[0] Add New User / Manual Entry")
    
    choice = input("\n🔢 Select User ID (or 0): ").strip()

    if choice in users and choice != "0":
        print(f"✅ Logged in as: {users[choice]['name']}")
        return users[choice]
    else:
        print("\n➕ Adding New User:")
        name = input("👤 Name: ").strip().title() 
        github = input("👤 GitHub URL: ").strip()
        telegram = input("✈️ Telegram ID (without @): ").strip()
        
        new_info = {"name": name, "github": github, "telegram": telegram}
        
        save_choice = input("❓ Save this user for future use? (y/n): ").lower()
        if save_choice == 'y':
            new_id = str(len(users) + 1)
            users[new_id] = new_info
            with open(users_path, "w", encoding="utf-8") as f:
                json.dump(users, f, indent=4, ensure_ascii=False)
            print(f"✨ User saved with ID: {new_id}")
            
        return new_info

def main():
    print("--- 🤖 Problem Auto-Doc Generator ---")

    # --- STEP 1: Pre-Check Connections ---
    print("\n🔍 Verifying connections...")
    tg_ok = check_telegram_connection()
    git_ok = check_git_connection()

    if not (tg_ok and git_ok):
        if not tg_ok: print("❌ CONNECTION ERROR: Telegram is unreachable.")
        if not git_ok: print("❌ CONNECTION ERROR: Git remote 'origin' not found.")
        print("⚠️ Process aborted to save API credits.")
        return
    print("✅ Connections checked successfully.")

    # --- STEP 2: Path Management ---
    bot_folder = os.path.dirname(os.path.abspath(__file__))
    repo_root = os.path.dirname(bot_folder) 
    problems_path = os.path.join(repo_root, "problems")

    # --- STEP 3: Scraper Setup ---
    url = input("\n🔗 Enter Problem URL: ").strip()
    author_data = get_author_info()

    if "codeforces.com" in url:
        scraper = CodeforcesScraper(url)
    elif "leetcode.com" in url:
        scraper = LeetCodeScraper(url)
    else:
        print("❌ Error: Unsupported platform URL.")
        return

    print("⏳ Scraping data...")
    data = scraper.extract_info()
    if not data or "error" in data:
        print("❌ Error: Scraping failed.")
        return
    data['author'] = author_data

    # --- STEP 4: Prepare Telegram Content (English) ---
    # We do this BEFORE translation to keep the message in English
    day_num = get_next_day_number(problems_path)
    github_repo = os.getenv("GITHUB_REPO_URL", "https://github.com/G-C-Club/Big-O-Daily")
    tg_message = format_telegram_message(data, day_num, github_repo)
    print("✅ English Telegram message prepared.")

    # --- STEP 5: AI Translation (For Persian README) ---
    print("🤖 Translating content for Persian README...")
    translator = AITranslator()
    try:
        translated_data = translator.translate_sections(data)
    except Exception as e:
        print(f"❌ Translation failed: {e}")
        return

    # --- STEP 6: Folder & Local File Management ---
    clean_title = data['title'].replace('/', '-').replace('\\', '-')
    folder_name = f"Day{day_num:04d} - {clean_title}"
    target_dir = os.path.join(problems_path, folder_name)
    os.makedirs(target_dir, exist_ok=True)
    
    english_md = generate_english_markdown(data)
    persian_md = generate_persian_markdown(translated_data)

    with open(os.path.join(target_dir, "README.md"), "w", encoding="utf-8") as f:
        f.write(english_md)
    with open(os.path.join(target_dir, "README-fa.md"), "w", encoding="utf-8") as f:
        f.write(persian_md)
    
    print(f"✅ Local files saved for Day {day_num:04d}")

    # --- STEP 7: Sync Database ---
    problem_entry = {
        "title": data['title'],
        "folder_path": f"./problems/{folder_name}",
        "link": url,
        "difficulty": data.get('difficulty', 'Unknown'),
        "platform": data['platform'],
        "tags": data['tags'],
        "author": data['author']
    }
    
    if update_database(problem_entry):
        sync_main_readme()

    # --- STEP 8: Final Publishing ---
    choice = input(f"\n🚀 Ready to publish Day {day_num:04d}. Commit and post? (y/n): ").strip().lower()
    
    if choice == 'y':
        # Send the previously prepared English message
        send_to_telegram(tg_message)
        
        # Git operations
        if git_commit_and_push(day_num, data['title']):
            print("\n✨ All tasks completed successfully!")
        else:
            print("\n⚠️ Telegram posted, but GitHub push failed.")
    else:
        print("\n⚠️ Action cancelled. Files are kept locally.")

if __name__ == "__main__":
    main()
