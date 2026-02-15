import cloudscraper
import re
import copy
from bs4 import BeautifulSoup, NavigableString
from .base_scraper import BaseScraper

class CodeforcesScraper(BaseScraper):
    def extract_info(self):
        match = re.search(r'(?:contest|problemset/problem)/(\d+)/(\w+)', self.url)
        if not match:
            return {"error": "Invalid URL format."}
        
        contest_id = match.group(1)
        problem_index = match.group(2)
        
        # ========================================================
        # 🔧 PROXY SETTINGS (SOCKS5 Fixed)
        # ========================================================
        PROXY_URL = "socks5://127.0.0.1:2080"
        
        proxies = {
            "http": PROXY_URL,
            "https": PROXY_URL
        }
        # ========================================================

        scraper = cloudscraper.create_scraper()

        result = {
            "title": f"{contest_id}{problem_index}",
            "difficulty": "Unknown",
            "tags": [],
            "link": self.url,
            "platform": "Codeforces",
            "header_info": {},    
            "statement": "",      
            "input_spec": "",     
            "output_spec": "",    
            "samples": [],        
            "note": ""            
        }

        try:
            print(f"   -> 🌍 Downloading HTML Content (Proxy: {PROXY_URL})...")
            response = scraper.get(self.url, proxies=proxies)
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                problem_statement = soup.find("div", class_="problem-statement")
                
                if problem_statement:
                    self._clean_mathjax(problem_statement)

                    header = problem_statement.find("div", class_="header")
                    if header:
                        # Extract raw title
                        raw_title = header.find("div", class_="title").get_text(strip=True)
                        
                        # --- FIX: Remove leading single letter and dot (e.g., "H. Title" -> "Title") ---
                        # Matches a single capital letter followed by a dot and optional spaces at start
                        clean_title = re.sub(r'^[A-Z]\.\s*', '', raw_title)
                        result['title'] = clean_title

                        time_limit = header.find("div", class_="time-limit")
                        if time_limit:
                            result['header_info']['time'] = list(time_limit.stripped_strings)[1]
                        mem_limit = header.find("div", class_="memory-limit")
                        if mem_limit:
                            result['header_info']['memory'] = list(mem_limit.stripped_strings)[1]
                        header.decompose()

                    sidebar_tags = soup.find_all("span", class_="tag-box")
                    result['tags'] = [t.text.strip() for t in sidebar_tags]
                    
                    sample_div = problem_statement.find("div", class_="sample-tests")
                    if sample_div:
                        result['samples'] = self._extract_samples(sample_div)
                        sample_div.decompose()

                    sections = {
                        "input-specification": "input_spec",
                        "output-specification": "output_spec",
                        "note": "note"
                    }
                    
                    main_text_parts = []
                    
                    for child in problem_statement.children:
                        if isinstance(child, NavigableString):
                            continue
                        
                        classes = child.get("class", [])
                        found_section = False
                        for cls_name, key in sections.items():
                            if cls_name in classes:
                                section_title = child.find("div", class_="section-title")
                                if section_title: section_title.decompose()
                                raw_text = self._html_to_markdown(child)
                                result[key] = self._final_clean(raw_text)
                                found_section = True
                                break
                        
                        if not found_section:
                            main_text_parts.append(self._html_to_markdown(child))
                    
                    full_statement = "\n\n".join(main_text_parts)
                    result['statement'] = self._final_clean(full_statement)
                    
                    print("   -> ✅ Scraping Complete!")
            else:
                print(f"   -> ❌ Failed with Status Code: {response.status_code}")
        except Exception as e:
            print(f"   -> ❌ Error: {e}")

        # Find tags in the sidebar
        sidebar_tags = soup.find_all("span", class_="tag-box")
        raw_tags = [t.text.strip() for t in sidebar_tags]

        # Filter tags and extract difficulty (e.g., *800)
        actual_tags = []
        difficulty = "Unknown"

        for tag in raw_tags:
            # Check if tag starts with '*' followed by a number
            if tag.startswith('*') and tag[1:].isdigit():
                difficulty = tag[1:] # Store as numerical difficulty
            else:
                actual_tags.append(tag)

        result['tags'] = actual_tags
        result['difficulty'] = difficulty

        return result

    def _final_clean(self, text):
        if not text: return ""
        text = re.sub(r'\$\$\$\s*(.*?)\s*\$\$\$', r'$\1$', text)
        text = text.replace("$$$", "$")
        text = text.replace(r'\le', r'\le ').replace(r'\ge', r'\ge ')
        return text.strip()

    def _clean_mathjax(self, soup):
        for junk in soup.find_all("span", class_=["MathJax_Preview", "MathJax", "MJX_Assistive_MathML"]):
            junk.decompose()
        for script in soup.find_all("script", type="math/tex"):
            latex = script.get_text()
            script.replace_with(f"${latex}$")
        for script in soup.find_all("script", type="math/tex; mode=display"):
            latex = script.get_text()
            script.replace_with(f"\n$${latex}$$\n")

    def _html_to_markdown(self, element):
        if element is None: return ""
        text = ""
        for child in element.children:
            if isinstance(child, NavigableString):
                content = str(child).strip()
                if content: text += content + " "
            else:
                tag = child.name
                content = self._html_to_markdown(child).strip()
                if tag == 'p': text += f"{content}\n\n"
                elif tag == 'ul': text += f"{content}\n"
                elif tag == 'li': text += f"- {content}\n"
                elif tag == 'pre': text += f"\n```\n{content}\n```\n"
                elif tag == 'span':
                    if "tex-font-style-tt" in child.get("class", []): text += f"`{content}` "
                    elif "tex-font-style-bf" in child.get("class", []): text += f"**{content}** "
                    elif "tex-font-style-it" in child.get("class", []): text += f"*{content}* "
                    else: text += f"{content} "
                else: text += f"{content} "
        return text

    def _extract_samples(self, sample_div):
        samples = []
        inputs = sample_div.find_all("div", class_="input")
        outputs = sample_div.find_all("div", class_="output")
        for inp, out in zip(inputs, outputs):
            pre_in = inp.find("pre")
            val_in = self._clean_pre_content(pre_in)
            pre_out = out.find("pre")
            val_out = self._clean_pre_content(pre_out)
            samples.append({"input": val_in, "output": val_out})
        return samples

    def _clean_pre_content(self, pre_tag):
        if not pre_tag: return ""
        temp = copy.copy(pre_tag)
        lines = temp.find_all("div", class_="test-example-line")
        if lines:
            return "\n".join([line.get_text().strip() for line in lines])
        for br in temp.find_all("br"):
            br.replace_with("\n")
        return temp.get_text().strip()
