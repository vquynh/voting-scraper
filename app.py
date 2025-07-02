from flask import Flask
import os
from scraper import run_scraper

app = run_scraper  # Import your function above

@app.route('/run', methods=['GET'])
def trigger():
    result = run_scraper()
    return result

if __name__ == '__main__':
    app.run()