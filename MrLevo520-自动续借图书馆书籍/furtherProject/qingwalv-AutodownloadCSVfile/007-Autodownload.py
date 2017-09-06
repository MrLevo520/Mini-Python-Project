from bs4 import BeautifulSoup
import requests

URL = 'http://cdn2.ime.sogou.com/9d502a2d322e1ce8f80489e2cff37720/59ad1252/dl/index/1502174063/sogou_pinyin_86b.exe'

def download_file(url, filename, headers):
    r = requests.get(url, stream=True, headers=headers)
    with open(filename, 'wb') as f:
        for chunk in r.iter_content(chunk_size=1024):
            if chunk:
                f.write(chunk)
                f.flush()

# get link and file name
response = requests.get(URL)
soup = BeautifulSoup(response.content)
a = soup.find('td', text='Download:').next_sibling.a
link = a.get('href')
filename = a.text + '.pdf'

# download file
headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2062.94 Safari/537.36',
    'Host': 'filepi.com',  # host could be extracted from the link
    'Referer': URL
}
download_file(link, filename, headers)