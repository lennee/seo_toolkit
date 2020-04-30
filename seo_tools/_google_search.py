#!usr/bin/python
import pandas as pd
import requests

from time import sleep
from pprint import pprint
from bs4 import BeautifulSoup
from urllib.request import urlopen, Request
from urllib.parse import quote_plus

'''

=====================
Conduct Google Search
=====================

Conducts a google search and returns a Pandas DataFrame of SERP
    Names and Domains

'''

def parseSERP(s, dat=None):
    try:
        t = s.find('h3').text
    except:
        t = None

    try:
        d = s.find('span', {'class': 'st'}).text
    except:
        d = None

    try:
        u = s.find('a')['href']
        if '/url?q=' in u:
            u = u.split('&')[0].replace('/url?q=','')
    except:
        u = None

    if dat is None:
        return {
            'title':t,
            'description':d,
            'url':u
        }
    else:
        dat['Title'].append(t)
        dat['Description'].append(d)
        dat['URL'].append(u)
        return dat

def _captchaCheck(u):
    res = requests.get(u)
    if res.status_code != 200:
        print('Something went wrong')
        if "To continue, please type the characters below:" in res.text:
            print('There is a Captcha check occuring')
            sleep(900);
            return True
        elif "your computer or network may be sending automated queries" in res.text:
            print('There is an automation check occuring')
            sleep(900);
            return True
        elif len(res.text)<10240:
            print('The page is oddly small')
            sleep(900);
            return True

def search(q, num=100):
    url = 'https://google.com/search?start=0&num=%i&q=%s' % (num, quote_plus(q))
    print(url)
    _captchaCheck(url)
    headers = {
        'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7'
        }
    req = Request(url,None,headers)
    try:
        serps = BeautifulSoup(urlopen(req), 'lxml').select('#search')[0].select('.g')
    except:
        raise Error('Could not read search data')
    data = {
        'Rank': [],
        'Query':[],
        'Title':[],
        'Description':[],
        'URL':[],
    }
    r = 0
    for s in serps:
        if s.select('.st') != [] and s.select('h3') != [] and s.select('a') != []:
            r += 1
            data['Rank'].append(r)
            data['Title'].append(s.select('h3')[0].text)
            data['Description'].append(s.select('.st')[0].text)
            u = s.select('a')[0]['href']
            if '/url?q=' in u:
                u = u.split('&')[0].replace('/url?q=','')
            data['URL'].append(u)

    data['Query'] = [q] * len(data['URL'])

    return pd.DataFrame(data).set_index('Rank')
