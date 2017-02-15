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
    '''Get picture from chitanka.com thumbnails'''

    print('getting picture for ', url)
    the_page = get(url)
    soup = BeautifulSoup(the_page, 'html.parser')

    div = soup.find_all('div', {'class': 'cover thumbnail'})[0]
    src = div.find_all('img')[0]['src']

    return re.sub(r'(.*\.)\d+(.jpg)$', r'http:\1max\2', src)

def base64_picture(url):
    try:
        img = get_picture(url)
        print('got picture: ' + img)
        return b64encode(get(img))
    except:
        return None # evil.
