from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from datetime import datetime
from zoneinfo import ZoneInfo
import time

def run_scraper():
    chrome_options = Options()
    chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--window-size=1280,720")
    chrome_options.add_argument("blink-settings=imagesEnabled=false")

    try:
        driver = webdriver.Chrome(options=chrome_options)
        url = "https://yvote.vn/voting-page/d49a70e5-e756-47a1-b70b-26d05e39592b?awardId=650505d3-c527-4869-a948-e9e214b51dbc"
        driver.get(url)

        print("Waiting for target element to be visible...")
        # Wait up to 20 seconds until the candidate name element is visible
        WebDriverWait(driver, 20).until(
            EC.visibility_of_element_located((By.CLASS_NAME, "MuiTypography-body1"))
        )

        print("Page fully loaded. Getting HTML...")

        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')

        # Your parsing logic
        name_elements = soup.find_all('p', class_="MuiTypography-root MuiTypography-body1")
        vote_elements = soup.find_all('p', class_="MuiTypography-root MuiTypography-inherit")

        results = []
        for name_elem, vote_elem in zip(name_elements, vote_elements):
            results.append({
                "name": name_elem.get_text(strip=True),
                "votes": vote_elem.get_text(strip=True)
            })
        print("🏆 Voting Results:")
        # Build JSON structure
        timestamp = datetime.now(ZoneInfo('Asia/Ho_Chi_Minh')).isoformat()
        result = {
            "timestamp": timestamp,
            "results": results
        }

        print("Scraped Results:", result)
        return result

    except Exception as e:
        print("Error during scraping:", str(e))
        return {"error": str(e)}

if __name__ == "__main__":
    run_scraper()