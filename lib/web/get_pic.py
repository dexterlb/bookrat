import urllib.request
from bs4 import BeautifulSoup
import re
from base64 import b64encode

def get(url):
    req = urllib.request.Request(url)
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:47.0) Gecko/20100101 Firefox/47.0')
    with urllib.request.urlopen(req) as response:
        return response.read()

def get_picture(url):
    the_page = get(url)
    soup = BeautifulSoup(the_page, 'html.parser')

    src = soup.find_all('img', {'alt': 'Корица', 'width': '200'})[0]['src']

    return re.sub(r'(.*)200(.jpg)$', r'http:\1max\2', src)

def base64_picture(url):
    img = get_picture(url)
    return b64encode(get(img))
