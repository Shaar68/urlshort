from flask import Flask, request, redirect, jsonify
import sqlite3, urllib3
import os

debugMode = False
if os.getenv("APP_DEBUG") == "true":
    debugMode = True

app = Flask(__name__)

def table_check():
    with sqlite3.connect('urls.db') as conn:
        c = conn.cursor()
        try:
            c.execute("CREATE TABLE WEB_URL (URL TEXT NOT NULL, KEY TEXT NOT NULL);")
            c.execute("CREATE TABLE API_KEYS (KEY TEXT NOT NULL);")
        except sqlite3.OperationalError:
            pass

def check_api_key(body):
    if 'api_key' not in body:
        return False

    with sqlite3.connect('urls.db') as conn:
        c = conn.cursor()
            
        result_cursor = c.execute('SELECT KEY FROM API_KEYS WHERE KEY=?', (body['api_key'],))
        if len(result_cursor.fetchall()) == 0:
            return False
        
    return True

@app.route('/create', methods=['POST'])
def create_url():
    body = request.get_json()
    orig_url = body['url']
    url_key = body['url_key']
   
    if not check_api_key(body):
        return 'error'

    with sqlite3.connect('urls.db') as conn:
        c = conn.cursor()
            
        result_cursor = c.execute('SELECT KEY FROM WEB_URL WHERE KEY=?', (url_key,))

        if len(result_cursor.fetchall()) > 0:
            return 'error: url already exists'
            
        result_cursor = c.execute('INSERT INTO WEB_URL (URL, KEY) VALUES (?, ?)', (orig_url, url_key))
        return url_key
        
    return 'error'

@app.route('/update', methods=['POST'])
def update_url():
    body = request.get_json()
    orig_url = body['url']
    url_key = body['url_key']
    
    if not check_api_key(body):
        return 'error'

    with sqlite3.connect('urls.db') as conn:
        c = conn.cursor()
            
        result_cursor = c.execute('SELECT KEY FROM WEB_URL WHERE KEY=?', (url_key,))

        if len(result_cursor.fetchall()) <= 0:
            return 'error: url does not exist'
            
        result_cursor = c.execute('UPDATE WEB_URL SET URL = ? WHERE key = ?', (orig_url, url_key))
        return url_key
        
    return 'error'

@app.route('/<url_key>')
def redirect_short_url(url_key):
    with sqlite3.connect('urls.db') as conn:
        c = conn.cursor()
        result_cursor = c.execute('SELECT URL FROM WEB_URL WHERE KEY=?', (url_key,))
        try:
            redirect_url = result_cursor.fetchone()[0]
        except Exception as e:
            print(e)
            return 'error'
    return redirect(redirect_url)

if __name__ == '__main__':
    table_check()
    app.run(debug=debugMode)