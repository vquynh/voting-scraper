from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time
import json
from datetime import datetime
from zoneinfo import ZoneInfo
import requests
import re

def run_scraper():

    # Use Firefox in headless mode
    options = Options()
    options.add_argument("--headless")
    driver = webdriver.Firefox(options=options)

    url = "https://yvote.vn/voting-page/d49a70e5-e756-47a1-b70b-26d05e39592b?awardId=650505d3-c527-4869-a948-e9e214b51dbc"
    driver.get(url)

    # Wait for JavaScript to load
    driver.implicitly_wait(2)

    # Get rendered HTML
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')

    # Now extract names and votes
    vote_class = "MuiTypography-root MuiTypography-inherit text-xs lg:text-xs font-semibold text-[#99999F]"
    name_class = "MuiTypography-root MuiTypography-body1 text-base lg:text-xl font-semibold text-white text-center"

    # Filter by exact class match
    def name_class_match(tag):
        return tag.name == 'p' and tag.get('class') and name_class in ' '.join(tag.get('class'))

    def vote_class_match(tag):
        return tag.name == 'p' and tag.get('class') and vote_class in ' '.join(tag.get('class'))

    name_elements = soup.find_all(name_class_match)
    vote_elements = soup.find_all(vote_class_match)

    print("🏆 Voting Results:")
    # Build JSON structure
    timestamp = datetime.now(ZoneInfo('Asia/Ho_Chi_Minh')).isoformat()
    results = {
        "timestamp": timestamp,
        "results": []
    }

    for name_elem, vote_elem in zip(name_elements, vote_elements):
        name = name_elem.get_text(strip=True)
        votes_text = vote_elem.get_text(strip=True)

        # Improved float extraction
        match = re.search(r"[-+]?\d*\.\d+|\d+", votes_text.replace(',', '.'))
        votes = float(match.group()) if match else 0.0


        results["results"].append({
            "name": name,
            "votes": votes
        })

    # Pretty print JSON locally
    print(json.dumps(results, ensure_ascii=False, indent=2))

    # Optional: Save to file
    with open("voting_results.json", "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)

    # 🔥 Send JSON to API
    api_url = "https://voting-dashboard-3q2r.onrender.com/api/submit-votes"
    headers = {
        "Content-Type": "application/json",
    }

    try:
        response = requests.post(api_url, json=results, headers=headers)
        response = requests.post(api_url, json=results)
        print(f"Posted to {api_url} | Status: {response.status_code}")
        return results

    except Exception as e:
        print("Error:", str(e))
        return {"error": str(e)}

    driver.quit()
if __name__ == "__main__":
    run_scraper()