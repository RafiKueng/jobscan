# -*- coding: utf-8 -*-
"""
Created on Mon Feb 16 22:01:59 2015

@author: rafik
"""

import requests
#import re
#import time
import bs4
from bs4 import BeautifulSoup as bs
#from datetime import datetime as dt


def getDetails(html):
    
    data = {}
    
    soup = bs(html)

    #data[] = soup.find(class_="header")
    s1 = soup.find(class_="vorspann").p
    if s1:
        data['firm'] = s1.text
    else:
        data['firm'] = '---'

    s2 = soup.find(class_="text")
    ps = s2.findAll('p')
    data['description'] = '\n'.join([p.text for p in ps])
    
    return data
    



se = requests.Session()

offers = {}

resp1 = se.get('https://www.unibas.ch/de/Mitarbeitendenportal/Aktuell/Offene-Stellen.html')



#cookies = {
#    'PHPSESSID': 'ace16jtl5ojm4rgd0n6bentkj6',
#    'basic_kombi': 'bgf3ohvg8e5nd4ber0pkk9u6a2',
#}

headers = {
    'Host': 'kombi.jobs.ch',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:31.0) Gecko/20100101 Firefox/31.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Accept-Encoding': 'gzip, deflate',
#    'Referer': 'https://kombi.jobs.ch/basic_kombi/?kid=unibas',
    'Connection': 'keep-alive',
}

data = {
    'kid':'unibas',
    'lng': 'de',
    'k': '',
    'c': '122',
    'r': '',
    'em': '',
    'pos': '',
    }

resp2 = se.post('https://kombi.jobs.ch/basic_kombi/index.php', headers=headers, data=data)

soup = bs(resp2.text)

itms = soup.table.tbody

counter = 0

for itm in itms.findAll('tr'):
    data = {}
    e = itm.findAll('td')
    comment = itm.findAll(text=lambda text:isinstance(text, bs4.Comment))[0]
    
    data['title'] = e[0].a.text
    data['link'] = e[0].a['href']
    
    data['location'] = e[1].text
    data['date'] = e[2].text
    
    data['category'] = bs(comment).text
    
    resp2 = se.get(data['link'])
    adddata = getDetails(resp2.text)
    
    data['adddata'] = adddata
    
    data['firm'] = adddata['firm']
    data['description']= adddata['description']
    
    offers[counter] = data
    print '%03i'%counter, data['title']
    counter += 1
    