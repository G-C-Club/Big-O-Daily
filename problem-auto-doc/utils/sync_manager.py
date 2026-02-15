import json
import os
from collections import Counter

def get_project_paths():
    """Calculate required paths relative to the script location in utils."""
    current_dir = os.path.dirname(os.path.abspath(__file__))
    # problem-auto-doc folder (where utils is located)
    bot_folder = os.path.dirname(current_dir) 
    # Root of the whole repository (parent of problem-auto-doc)
    repo_root = os.path.dirname(bot_folder) 
    
    # Path to the 'data' folder inside 'problem-auto-doc'
    data_folder = os.path.join(bot_folder, "data")
    
    if not os.path.exists(data_folder):
        os.makedirs(data_folder)
        
    return {
        "db": os.path.join(data_folder, "database.json"),
        "readme": os.path.join(repo_root, "README.md"), # Main README is in Repo Root
        "problems": os.path.join(repo_root, "problems") # Problems folder is in Repo Root
    }
def update_database(new_entry):
    """Add a new problem entry to the JSON database."""
    paths = get_project_paths()
    data = []
    
    if os.path.exists(paths["db"]):
        with open(paths["db"], "r", encoding="utf-8") as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError:
                data = []

    # Prevent duplicate entries based on the folder path
    if not any(item['folder_path'] == new_entry['folder_path'] for item in data):
        data.append(new_entry)
        with open(paths["db"], "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
        return True
    return False

def generate_leaderboard(data):
    """Generate the leaderboard table based on the number of solved problems."""
    authors_count = Counter(item['author']['name'] for item in data)
    # Sort: highest number of solved problems at the top
    sorted_authors = sorted(authors_count.items(), key=lambda x: x[1], reverse=True)

    md = "## 🏆 Leaderboard\n\n"
    md += "| Rank | Author | Solved Problems | Profile |\n"
    md += "| :--- | :--- | :---: | :--- |\n"

    for rank, (name, count) in enumerate(sorted_authors, 1):
        # Find the first record of the author to extract profile links
        auth_info = next(item['author'] for item in data if item['author']['name'] == name)
        github_link = f"[🐙]({auth_info['github']})"
        tg_link = f" [✈️](https://t.me/{auth_info['telegram']})" if auth_info.get('telegram') else ""
        
        md += f"| {rank} | **{name}** | {count} | {github_link}{tg_link} |\n"
    
    return md

def generate_problems_table(data):
    """Generate the comprehensive list of all solved problems."""
    md = "## 📚 All Problems\n\n"
    md += "| # | Title | Author | Difficulty | Platform | Tags | Link |\n"
    md += "| :--- | :--- | :--- | :---: | :---: | :--- | :---: |\n"

    for idx, item in enumerate(data, 1):
        title_link = f"[{item['title']}]({item['folder_path']})"
        author_link = f"[{item['author']['name']}]({item['author']['github']})"
        tags = " ".join([f"`{t}`" for t in item.get('tags', [])])
        
        md += f"| {idx} | {title_link} | {author_link} | {item['difficulty']} | {item['platform']} | {tags} | [🔗]({item['link']}) |\n"
    
    return md

def sync_main_readme():
    """Overwrite the main README.md file in the project root."""
    paths = get_project_paths()
    
    if not os.path.exists(paths["db"]):
        print("⚠️ Database file not found.")
        return

    with open(paths["db"], "r", encoding="utf-8") as f:
        data = json.load(f)

    # --- Header Section ---
    header = "# 🚀 GCC - Big-O Daily Solutions\n\n"

    badges = [
        "[![GCC Channel](https://img.shields.io/badge/GCC_Club-Channel-blue?style=for-the-badge&logo=telegram)](https://t.me/GCC_IUT)",
        "[![Big-O Daily](https://img.shields.io/badge/Big--O_Daily-Questions-blue?style=for-the-badge&logo=telegram)](https://t.me/Big_O_Daily)",
        "[![Submit Solution](https://img.shields.io/badge/Submit_Solution-Javad-green?style=for-the-badge&logo=telegram)](https://t.me/javadabdolahi)"
    ]
    
    header += " ".join(badges) + "\n\n"
    
    header += "This repository contains daily problem solutions from **GCC** members.\n\n"
    
    # --- Table of Contents Section ---
    header += "### 📌 Contents\n"
    header += "1. [🏆 Leaderboard](#-leaderboard)\n"
    header += "2. [📚 All Problems](#-all-problems)\n"
    header += "3. [🤖 About the Bot](#updated-by-auto-sync-manager-)\n\n"
    header += "---\n\n"
    
    leaderboard = generate_leaderboard(data)
    problems_table = generate_problems_table(data)
    
    footer = "\n\n---\n*Updated by Auto-Sync Manager 🤖*"
    
    with open(paths["readme"], "w", encoding="utf-8") as f:
        f.write(header + leaderboard + "\n\n" + problems_table + footer)
    
    print("✅ Main README.md with TOC has been successfully updated.")
