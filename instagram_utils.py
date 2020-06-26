
import json
from datetime import datetime

import bs4
import requests


def get_insta_post(id: str):
    api_url = f'https://instagram.com/tv/{id}'
    soup = bs4.BeautifulSoup(requests.get(api_url).content, 'html.parser')

    raw_text = soup.body.script.string.strip()

    # Get rid of 'window._sharedData =' at front and ';' at back
    start = raw_text.find('=')
    end = raw_text.rfind(';')

    js = json.loads(raw_text[start + 1:end])
    return js['entry_data']['PostPage'][0]['graphql']['shortcode_media']