from flask import Flask
import asyncio
from scraper import run_scraper

app = Flask(__name__)

@app.route('/run')
def trigger_scrape():
    result = asyncio.run(run_scraper())
    return result

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)