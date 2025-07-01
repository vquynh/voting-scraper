from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time
import json
from datetime import datetime
import requests
import re


# Setup Chrome options
chrome_options = Options()
chrome_options.add_argument("--headless")  # Run in headless mode (no browser window)
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")

# Start browser
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

url = "https://yvote.vn/voting-page/d49a70e5-e756-47a1-b70b-26d05e39592b?awardId=650505d3-c527-4869-a948-e9e214b51dbc"
driver.get(url)

# Wait for JavaScript to load
time.sleep(2)  # You can increase this if needed

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
timestamp = datetime.now().isoformat()
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
    print(f"API Response Status Code: {response.status_code}")
    print("API Response Body:", response.text)
except Exception as e:
    print("Error sending data to API:", e)

driver.quit()