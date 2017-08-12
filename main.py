from flask import Flask, request, redirect, jsonify
import sqlite3
import urllib3
import uuid
import os
import aetea_base as base

debugMode = False
if os.getenv("APP_DEBUG") == "true":
    debugMode = True

port = int(os.getenv("APP_PORT", "80"))
base_url = os.getenv("APP_BASE_URL")

app = Flask(__name__)

def table_check():
    with sqlite3.connect('urls.db') as conn:
        c = conn.cursor()
        try:
            c.execute("CREATE TABLE WEB_URL (URL TEXT NOT NULL, KEY TEXT NOT NULL);")
            c.execute("CREATE TABLE API_KEYS (KEY TEXT NOT NULL);")
        except sqlite3.OperationalError:
            pass

def create_new_url(orig_url, key=None):
    if key is None:
        key = base.encode(uuid.uuid4().int)[:8]

    with sqlite3.connect('urls.db') as conn:
        c = conn.cursor()
        
        result_cursor = c.execute('SELECT KEY FROM WEB_URL WHERE KEY=?', (key,))

        if len(result_cursor.fetchall()) > 0:
            return (False, None)
            
        result_cursor = c.execute('INSERT INTO WEB_URL (URL, KEY) VALUES (?, ?)', (orig_url, key))
        return (True, key)
        
    return (False, None)

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

    status = create_new_url(orig_url, key=url_key)
    
    if status is True:
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

@app.route('/new')
def new_url_random():
    orig_url = request.args.get('url')

    with sqlite3.connect('urls.db') as conn:
        c = conn.cursor()
        
        result_cursor = c.execute('SELECT KEY FROM WEB_URL WHERE URL=?', (orig_url,))

        fetched = result_cursor.fetchall()
        if len(fetched) > 0:
            return base_url + fetched[0][0]
        
        status, key = create_new_url(orig_url)

        if status is True:
            return base_url + key
            
        return 'error'

@app.route('/')
def home():
    return 'Aetea\'s little url shortener: <a href="https://github.com/aetea/urlshort">GitHub</a>'

if __name__ == '__main__':
    table_check()
    app.run(host='0.0.0.0', debug=debugMode, port=port)