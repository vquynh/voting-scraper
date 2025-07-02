import os
import asyncio
from bs4 import BeautifulSoup
from playwright.async_api import async_playwright
from zoneinfo import ZoneInfo
from datetime import datetime

async def run_scraper():
    url = "https://yvote.vn/voting-page/d49a70e5-e756-47a1-b70b-26d05e39592b?awardId=650505d3-c527-4869-a948-e9e214b51dbc"

    try:
        async with async_playwright() as p:
            print("Launching browser...")
            browser = await p.chromium.launch(headless=True)
            page = await browser.new_page()

            print(f"Navigating to {url}...")
            await page.goto(url, wait_until="domcontentloaded")

            # Wait for JS-rendered content (update selector if needed)
            print("Waiting for voting elements...")
            await page.wait_for_selector("p.MuiTypography-body1", timeout=30000)

            # Optional: Scroll to trigger lazy loading
            await page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
            await asyncio.sleep(3)

            # Get rendered HTML
            html = await page.content()
            soup = BeautifulSoup(html, 'html.parser')

            name_elements = soup.find_all('p', class_="MuiTypography-root MuiTypography-body1")
            vote_elements = soup.find_all('p', class_="MuiTypography-root MuiTypography-inherit")

            results = []
            for name_elem, vote_elem in zip(name_elements, vote_elements):
                name = name_elem.get_text(strip=True)
                votes = vote_elem.get_text(strip=True)
                results.append({
                    "name": name,
                    "votes": votes
                })

            print("🏆 Voting Results:")
            # Build JSON structure
            timestamp = datetime.now(ZoneInfo('Asia/Ho_Chi_Minh')).isoformat()
            result = {
                "timestamp": timestamp,
                "results": results
            }

            print("Scraped Results:", results)
            await browser.close()
            return result

    except Exception as e:
        print("Error during scraping:", str(e))
        return {"error": str(e)}