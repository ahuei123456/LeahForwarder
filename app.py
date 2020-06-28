"""
This script runs the application using a development server.
It contains the definition of routes and views for the application.
"""

import json
from datetime import datetime

import bs4
import requests

from flask import Flask
app = Flask(__name__)

# Make the WSGI interface available at the top level so wfastcgi can get it.
wsgi_app = app.wsgi_app

def get_insta_js(api_url: str):
    
    soup = bs4.BeautifulSoup(requests.get(api_url).content, 'html.parser')

    raw_text = soup.body.script.string.strip()

    # Get rid of 'window._sharedData =' at front and ';' at back
    start = raw_text.find('=')
    end = raw_text.rfind(';')

    js = json.loads(raw_text[start + 1:end])
    return js


def get_insta_post(id: str):
    api_url = f'https://instagram.com/tv/{id}'

    js = get_insta_js(api_url)
    return js['entry_data']['PostPage'][0]['graphql']['shortcode_media']


def get_insta_user(id: str):
    api_url = f'https://instagram.com/{id}'

    js = get_insta_js(api_url)
    return js['entry_data']['ProfilePage'][0]['graphql']['user']


@app.route('/')
def hello():
    """Renders a sample page."""
    return "Hello World!"

@app.route('/hello')
def hello1():
    return "goodbye world"

@app.route('/instagram/tv/<id>')
@app.route('/instagram/p/<id>')
def insta_raw(id: str):
    return get_insta_post(id)

@app.route('/instagram/<id>')
def insta_user(id: str):
    return get_insta_user(id)

@app.route('/instagram')
def insta_test():
    return 'i love ice'

if __name__ == '__main__':
    import os
    HOST = os.environ.get('SERVER_HOST', 'localhost')
    try:
        PORT = int(os.environ.get('SERVER_PORT', '7777'))
    except ValueError:
        PORT = 7777
    app.run(HOST, PORT)
