from flask import Flask, request, jsonify
from playwright.sync_api import sync_playwright
import os
import threading

app = Flask(__name__)
lock = threading.Lock()

@app.route('/scrape', methods=['POST'])
def scrape():
    data = request.get_json()
    url = data.get('url', '')
    
    if not url:
        return jsonify({'html': '', 'error': 'URL required'}), 400
    
    with lock:
        try:
            with sync_playwright() as p:
                browser = p.chromium.launch(
                    headless=True,
                    args=['--no-sandbox', '--disable-setuid-sandbox', '--disable-dev-shm-usage', '--single-process']
                )
                page = browser.new_page()
                page.goto(url, wait_until='domcontentloaded', timeout=15000)
                html = page.content()
                browser.close()
                return jsonify({'html': html})
        except Exception as e:
            return jsonify({'html': '', 'error': str(e)}), 500

@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'ok'})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port, threaded=False)
