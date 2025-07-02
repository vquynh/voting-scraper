from flask import Flask
import os
from scraper import run_scraper

app = Flask(__name__)

@app.route('/')
def home():
    return "Use /run to start the scraper"

@app.route('/run', methods=['GET'])
def trigger():
    result = run_scraper()
    return result

if __name__ == '__main__':
    app.run()