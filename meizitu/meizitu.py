import requests
from bs4 import BeautifulSoup as bs
from urllib import request as urllib2

for i in range(6,71):
    url = 'http://www.mmjpg.com/home/{}'.format(str(i))
    html = bs(requests.get(url).content,
              'html.parser')
    li = html.find_all(name = 'li')
    for x in li:
        url = x.find(name = 'a')['href']
        html = bs(requests.get(url).content,
                  'html.parser')
        picinfo = html.find(name = 'div',
                            attrs = {'class':'clearfloat'}).\
                            get_text()
        picinfo = picinfo[14:].\
                  strip(';').\
                  strip('[').\
                  strip(']').\
                  split(',')
        for i in range(1,int(picinfo[2])+1):
            url = 'http://img.mmjpg.com/' + \
                  picinfo[0] + '/' + \
                  picinfo[1] + '/' + \
                  str(i) +'.jpg'
            urllib2.urlretrieve(url,picinfo[0] +
                                picinfo[1] +
                                str(i) + '.jpg')
