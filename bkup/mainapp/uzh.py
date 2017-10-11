# -*- coding: utf-8 -*-
"""
Created on Mon Feb 16 00:33:49 2015

@author: rafik
"""

import requests
#import re
#import time
from bs4 import BeautifulSoup as bs
from datetime import datetime as dt

offers = {}



def getDetails(lnk):
    
    soup = bs(se.get(lnk).text)
    cont = soup.find(class_="content")
    lst = [_ for _ in cont.children if _ not in [ '\n',' ']]

    data = {}
    
    data['title'] = lst.pop(0).text
    data['date'] = dt.date(dt.strptime(lst.pop(0).text.split(':')[1].strip(), '%d.%m.%Y'))
    
    while len(lst)>0:
        e1 = lst.pop(0)
        if e1.name and e1.name.startswith('h'):
            key = e1.text
            val = lst.pop(0).text
            if lst[0].name == 'p': #special case with "bewerbungen"
                val += '\n'+lst.pop(0).text
        else:
            key = u'id'
            val = e1.strip()
        data[key] = val
    return data





se = requests.Session()
resp1 = se.get('http://www.jobs.uzh.ch')


page = 0
counter = 0
while True:
    
    headers = {
        'Host': 'www.jobs.uzh.ch',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:31.0) Gecko/20100101 Firefox/31.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate',
#        'Referer': 'http://www.jobs.uzh.ch/index.php?pageNum_rsJobs=1&&totalRows_rsJobs=44&rubrik=4%2C7%2C2%2C9%2C3',
        'Connection': 'keep-alive',
    }
    
    resp3 = se.get('http://www.jobs.uzh.ch/index.php?pageNum_rsJobs='+str(page)+'&rubrik=4%2C7%2C2%2C9%2C3', headers=headers)
    
    soup = bs(resp3.text)
    lst = soup.findAll(class_="ornate")[0].findAll('tr')[1:] # exclude header
    
    if len(lst) ==0:
        break
    
    for itm in lst:
        data = {}
        
        elems = itm.findAll('td')
        
        data['title'] = elems[0].a.text.strip()
        data['link_jobdetails'] = 'http://www.jobs.uzh.ch/' + elems[0].a['href']
        
        data['percentage'] = elems[1].text

        data['firm'] = elems[2].text

        data['date_published'] = dt.date(dt.strptime(elems[3].text, '%d.%m.%Y'))
    

        adddata = getDetails(data['link_jobdetails'])
        data['adddata'] = adddata
        data['description'] = 'Aufgabenbereich: ' + adddata.get('Aufgabenbereich', '---') + '\nAnforderungen: ' + adddata.get('Anforderungen','---')
        data['date_jobstart'] = adddata.get('Stellenantritt', '---')


        offers[counter] = data
        print '%03i'%counter, '%-30s' % data['title'][:30] 
        counter += 1
    page += 1
    
 
