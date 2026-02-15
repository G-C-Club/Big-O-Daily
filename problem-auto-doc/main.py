import os
from scrapers.codeforces import CodeforcesScraper
from services.ai_translator import AITranslator
from utils.file_manager import generate_english_markdown, generate_persian_markdown, get_next_day_number
from utils.telegram_sender import format_telegram_message, send_to_telegram, check_telegram_connection
from utils.git_manager import check_git_connection, git_commit_and_push

def main():
    print("--- 🤖 Problem Auto-Doc Generator ---")

    # --- STEP 1: Pre-Check Connections (To save API Quota) ---
    print("\n🔍 Verifying connections before processing...")
    tg_ok = check_telegram_connection()
    git_ok = check_git_connection()

    if not (tg_ok and git_ok):
        if not tg_ok: 
            print("❌ CONNECTION ERROR: Telegram is unreachable. Check Token/Channel ID.")
        if not git_ok: 
            print("❌ CONNECTION ERROR: Git remote 'origin' not found. Initialize git first.")
        print("⚠️ Process aborted to save API credits.")
        return

    print("✅ Connections verified. Proceeding to scrape...")

    # --- STEP 2: Input and Scraping ---
    url = input("\n🔗 Enter Problem URL: ")
    scraper = CodeforcesScraper(url)
    translator = AITranslator()

    try:
        # 1. Scrape data
        data = scraper.extract_info()
        if not data or "error" in data:
            print("❌ Error: Scraping failed.")
            return

        # 2. AI Processing (Translation happens here)
        print("   -> 📝 Preparing English and Persian content...")
        english_content = generate_english_markdown(data)
        translated_data = translator.translate_sections(data)
        persian_content = generate_persian_markdown(translated_data)

        # 3. Path Management
        project_root = os.path.dirname(os.path.abspath(__file__))
        parent_dir = os.path.dirname(project_root)
        problems_path = os.path.join(parent_dir, "problems")
        
        day_num = get_next_day_number(problems_path)
        clean_title = data['title'].replace('/', '-').replace('\\', '-')
        target_dir = os.path.join(problems_path, f"Day{day_num:04d} - {clean_title}")

        # 4. Save files locally
        os.makedirs(target_dir, exist_ok=True)
        with open(os.path.join(target_dir, "README.md"), "w", encoding="utf-8") as f:
            f.write(english_content)
        with open(os.path.join(target_dir, "README-fa.md"), "w", encoding="utf-8") as f:
            f.write(persian_content)
        
        print(f"✅ Local files saved for Day {day_num:04d}")

        # 5. Final Confirmation for Publishing
        print(f"\n🚀 Ready to publish: Day {day_num:04d} - {data['title']}")
        choice = input(f"❓ Commit to GitHub and post to Telegram? (y/n): ").strip().lower()
        
        if choice == 'y':
            # Post to Telegram
            github_repo = os.getenv("GITHUB_REPO_URL")
            tg_message = format_telegram_message(data, day_num, github_repo)
            send_to_telegram(tg_message)
            
            # Push to GitHub
            if git_commit_and_push(day_num, data['title']):
                print("\n✨ All tasks completed successfully!")
            else:
                print("\n⚠️ Telegram posted, but GitHub push failed.")
        else:
            print("\n⚠️ Action cancelled. Files are kept locally.")

    except Exception as e:
        print(f"\n❌ Critical Error: {e}")

if __name__ == "__main__":
    main()
