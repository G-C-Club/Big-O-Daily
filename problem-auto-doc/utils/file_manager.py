import os
import re

def generate_english_markdown(data):
    """
    Constructs the enhanced English README with navigation, 
    integrated details table, and hyperlinked source.
    """
    # Navigation link to the Persian version
    md = "[🇮🇷 Persian Version](./README-fa.md)\n\n"
    
    # Problem Title and Hyperlinked Source
    md += f"# Question: {data.get('title', 'Problem Title')}\n"
    md += f"[**🔗 Problem Link**]({data.get('link', '#')})\n\n"
    
    # Combined Technical Details and Tags Table
    md += "### ⚙️ Details\n"
    md += "| Feature | Specification |\n"
    md += "| :--- | :--- |\n"
    
    # Add standard header info (Time/Memory) to the table
    if 'header_info' in data:
        for key, value in data['header_info'].items():
            md += f"| **{key.capitalize()}** | {value} |\n"
    
    # Include tags as a row in the same table
    if data.get('tags'):
        tags_str = ", ".join([f"`{tag}`" for tag in data['tags']])
        md += f"| **Tags** | {tags_str} |\n"
    
    md += "\n---\n"

    md += "### 📖 Description\n"
    md += f"{data.get('statement', '')}\n\n"

    if data.get('input_spec'):
        md += "### 📥 Input Specification\n"
        md += f"{data.get('input_spec')}\n\n"
    
    if data.get('output_spec'):
        md += "### 📤 Output Specification\n"
        md += f"{data.get('output_spec')}\n\n"

    md += "---\n"

    if data.get('samples'):
        md += "### 🧪 Samples\n"
        for i, sample in enumerate(data['samples']):
            md += f"#### Sample {i+1}\n"
            md += "| Input | Output |\n"
            md += "| :--- | :--- |\n"
            # Format newlines for markdown table compatibility
            inp = sample['input'].replace('\n', '<br>')
            out = sample['output'].replace('\n', '<br>')
            md += f"| <pre>{inp}</pre> | <pre>{out}</pre> |\n\n"

    if data.get('note'):
        md += "### 📝 Note\n"
        md += f"{data.get('note')}\n\n"

    # Bot footer note
    md += "\n---\n"
    md += "*Note: These problem statements have been automatically retrieved by the bot.*"
    return md

def generate_persian_markdown(data):
    """
    Constructs the enhanced Persian README with full RTL support, 
    navigation, and integrated details table.
    """
    # Navigation link to the English version
    md = "[🇺🇸 English Version](./README.md)\n\n"
    
    # Start Global RTL Wrapper for Persian content
    md += '<div dir="rtl" align="right">\n\n'
    
    # Problem Title and Hyperlinked Source
    md += f"# سوال: {data.get('title', 'عنوان سوال')}\n"
    md += f" [**🔗 لینک سوال**]({data.get('link', '#')})\n\n"
    
    # Details and Tags Table in Persian
    md += "### ⚙️ جزئیات\n"
    md += "| ویژگی | مقدار |\n"
    md += "| :--- | :--- |\n"
    
    if 'header_info' in data:
        for key, value in data['header_info'].items():
            # Translate common headers for a better Persian UI
            translated_key = "زمان" if key.lower() == "time" else "حافظه" if key.lower() == "memory" else key.capitalize()
            md += f"| **{translated_key}** | {value} |\n"
    
    if data.get('tags'):
        tags_str = ", ".join([f"`{tag}`" for tag in data['tags']])
        md += f"| **تگ‌ها** | {tags_str} |\n"
        
    md += "\n---\n"
    
    md += "### 📖 صورت سوال\n"
    md += f"{data.get('statement', '')}\n\n"

    if data.get('input_spec'):
        md += "### 📥 مشخصات ورودی\n"
        md += f"{data.get('input_spec', '')}\n\n"
    
    if data.get('output_spec'):
        md += "### 📤 مشخصات خروجی\n"
        md += f"{data.get('output_spec', '')}\n\n"

    # Close RTL div for samples as code/numbers are better shown LTR
    md += "</div>\n\n---\n"

    if data.get('samples'):
        md += "### 🧪 نمونه‌ها\n"
        for i, sample in enumerate(data['samples']):
            md += f"#### نمونه {i+1}\n"
            md += "| ورودی (Input) | خروجی (Output) |\n"
            md += "| :--- | :--- |\n"
            inp = sample['input'].replace('\n', '<br>')
            out = sample['output'].replace('\n', '<br>')
            md += f"| <pre>{inp}</pre> | <pre>{out}</pre> |\n\n"

    # Re-open RTL div for notes and footer
    md += '<div dir="rtl" align="right">\n\n'
    
    if data.get('note'):
        md += "### 📝 نکات\n"
        md += f"{data.get('note', '')}\n\n"

    md += "---\n"
    md += "*توجه: این صورت سوال‌ توسط ربات دریافت و ترجمه شده است.*"
    md += "\n\n</div>\n"

    return md

def get_next_day_number(base_path=None):
    """
    Calculates the next available Day folder number in a directory 
    located next to the project folder.
    """
    if base_path is None:
        # Get the directory of the current file (utils)
        current_dir = os.path.dirname(os.path.abspath(__file__)) 
        # Go up to the project root (problem-auto-doc)
        project_root = os.path.dirname(current_dir) 
        # Go up to the parent directory (where problems should be)
        parent_dir = os.path.dirname(project_root) 
        base_path = os.path.join(parent_dir, "problems")

    if not os.path.exists(base_path):
        os.makedirs(base_path)
        return 1
    
    # List folders starting with 'Day'
    folders = [f for f in os.listdir(base_path) if f.startswith("Day")]
    if not folders:
        return 1
    
    day_numbers = []
    for f in folders:
        match = re.search(r'Day(\d+)', f)
        if match:
            day_numbers.append(int(match.group(1)))
    
    return max(day_numbers) + 1 if day_numbers else 1
