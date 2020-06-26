"""
This script runs the application using a development server.
It contains the definition of routes and views for the application.
"""

from flask import Flask
app = Flask(__name__)

from instagram_utils import *

# Make the WSGI interface available at the top level so wfastcgi can get it.
wsgi_app = app.wsgi_app


@app.route('/')
def hello():
    """Renders a sample page."""
    return "Hello World!"

@app.route('/hello')
def hello1():
    return "goodbye world"

@app.route('/instagram/<id>')
def insta_raw(id: str):
    return get_insta_post(id)

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
