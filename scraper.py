from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time
import json
from datetime import datetime
from zoneinfo import ZoneInfo
import requests
import re

def run_scraper():

        # Setup Firefox options
    firefox_options = Options()
    firefox_options.add_argument("--headless")  # Run in headless mode
    firefox_options.add_argument("--no-sandbox")
    firefox_options.add_argument("--disable-dev-shm-usage")

    # Start Firefox driver
    driver = webdriver.Firefox(options=firefox_options)

    url = "https://yvote.vn/voting-page/d49a70e5-e756-47a1-b70b-26d05e39592b?awardId=650505d3-c527-4869-a948-e9e214b51dbc"

    # Wait for JavaScript to load
    try:
        print("Navigating to page...")
        driver.get(url)

        # Wait for a known element to appear (update this class name)
        print("Waiting for content to load...")
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CLASS_NAME, "MuiTypography-body1"))
        )

        # Optional: Scroll to trigger JS rendering
        print("Scrolling to load more content...")
        last_height = driver.execute_script("return document.body.scrollHeight")
        while True:
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height

        # Get fully rendered HTML
        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')


        # Now extract names and votes
        name_class_pattern = "MuiTypography-root MuiTypography-body1 text-base lg:text-xl font-semibold text-white text-center"
        vote_class_pattern = "MuiTypography-root MuiTypography-inherit text-xs lg:text-xs font-semibold text-[#99999F]"

        def name_match(tag):
            return tag.name == 'p' and tag.has_attr('class') and ' '.join(tag['class']).startswith(name_class_pattern)

        def vote_match(tag):
            return tag.name == 'p' and tag.has_attr('class') and ' '.join(tag['class']).startswith(vote_class_pattern)

        name_elements = soup.find_all(name_match)
        vote_elements = soup.find_all(vote_match)

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
    
        response = requests.post(api_url, json=results, headers=headers)
        print(f"Posted to {api_url} | Status: {response.status_code}")
        return results

    except Exception as e:
        print("Error:", str(e))
        return {"error": str(e)}

    finally:
        driver.quit()
if __name__ == "__main__":
    run_scraper()