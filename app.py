from flask import Flask
from scraper import run_scraper

app = Flask(__name__)

@app.route('/run', methods=['GET'])
def trigger():
    result = run_scraper()
    return result

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)