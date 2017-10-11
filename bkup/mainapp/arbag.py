'''
jobboerse.arbeitsagentur.de

'''



import requests
import re
import time
from bs4 import BeautifulSoup as bs
from datetime import datetime as dt

se = requests.Session()


offers = {}
avail_keys = {}
counter = 0
log = []


def parse_string(el):
   text = ''.join(el.findAll(text=True))
   return text.strip()


def parseResultPage(html):
    bsall = bs(html)
    bstbl = bsall.table
    if not bstbl:
        return False
    bsrows = bstbl.find_all('tr')
    
    global offers
    global resp3a
    global dataa
    global adddata
    global counter
    global row

    for row in bsrows:
        
        data = {}
        dataa = data

        cols = row.find_all('td')
        if len(cols)<4: # can be 0 for special cases?; can be 1 for t header "aehnliche stellenangebote" 
            continue
        
        data["title"] = cols[1].a.span.text
        link2details = cols[1].a['href']
        data['link_jobdetails'] = 'http://jobboerse.arbeitsagentur.de' + link2details
        
        data['date_published'] = dt.date(dt.strptime(cols[2].span.text, '%d.%m.%Y'))

        #print str(cols[3])+'\n\n'
        try:
            t = cols[3].a.text
        except AttributeError:
            t = parse_string(cols[3])
        data['firm'] = t

        plzloc = cols[4].div.text.split()
        if plzloc[0].isdigit():
            plz = plzloc[0]
            loc = " ".join(plzloc[1:])
        else:
            plz=None
            loc = " ".join(plzloc)
        data['work_location'] = { 'plz': plz, 'loc': loc }
        
        data['distance_to_home'] = cols[5].span.text
        
        try:
            t = dt.date(dt.strptime(cols[6].div.text.strip(), '%d.%m.%Y'))
        except ValueError:
            t = cols[6].div.text.strip()
        data['date_jobstart'] = t

#        adddata = {}
#        if 'redirect_extern' not in link2details:
#            resp3a = se.get(data['link_jobdetails'])
#            adddata = getJobDetails(resp3a.text)
        
#        data['adddata'] = adddata
#        data['description'] = adddata.get('Stellenbeschreibung', '---')
        

        logstr = ' | '.join(['%03i'%counter, '%-40s' % data['title'][:40] ])
        print logstr
        log.append(logstr)
        offers[counter] = data
        counter +=1
        
    return True





def getJobDetails(html):
    soup = bs(html)
    
    # Helper function to return concatenation of all character data in an element

    data = {}
    for box in soup.find_all(class_='klappbar'):
        entries = box.find_all(class_="cf")
        
        
        for entry in entries:
            #print str(''.join(str(entry).split())) + '\n'
            cld = entry.findChildren()
            if len(cld)<2: continue
            title = cld[0].text.strip()
            tmp = parse_string(cld[1])
            tmp = tmp.replace('\t', '')
            tmp = re.sub( '\n+', '\n', tmp ).strip()
            text = tmp

            #print title,"|", text
            
            if len(title)==0 and text.startswith("Branche:"):
                i_bg = text.find(u'Betriebsgr')
                data[u'Branche'] = text[9:i_bg]
                data[u'Betriebsgr\xf6sse'] = text[i_bg+15:]
                continue
            
            avail_keys[title] = True
            data[title] = text
            
    return data







headers = {
    'Host': 'jobboerse.arbeitsagentur.de',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:31.0) Gecko/20100101 Firefox/31.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Accept-Encoding': 'gzip, deflate',
    'Connection': 'keep-alive',
    'Pragma': 'no-cache',
    'Cache-Control': 'no-cache',
}

resp1 = se.get('http://jobboerse.arbeitsagentur.de/', headers=headers)






cookies = {
#    'expires': 'Sun, 15 Feb 2015 15:03:29 GMT',
}

headers = {
    'Host': 'jobboerse.arbeitsagentur.de',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:31.0) Gecko/20100101 Firefox/31.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Accept-Encoding': 'gzip, deflate',
    'Referer': 'http://jobboerse.arbeitsagentur.de/',
    'Connection': 'keep-alive',
    'Pragma': 'no-cache',
    'Cache-Control': 'no-cache',
}

data = {
    'sieSuchen.wert.wert': 'leer',
    'suchbegriff.wert': '',
    'arbeitsort.lokation': '',
    '_eventId_erweitertesuche': 'Erweiterte+Suche'
}

resp2 = se.post('http://jobboerse.arbeitsagentur.de/vamJB/schnellsuche.html', headers=headers, cookies=cookies, data=data)






cookies = {
#    'allgemeineSuchkriterien.eingeklappt': '1',
#    'weitereSuchkriterien.eingeklappt': '0',
#    'expires': 'Sun, 15 Feb 2015 15:03:29 GMT',
#    'jsessionid': se.cookies['jsessionid'],
}

headers = {
    'Host': 'jobboerse.arbeitsagentur.de',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:31.0) Gecko/20100101 Firefox/31.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Accept-Encoding': 'gzip, deflate',
#    'Referer': 'http://jobboerse.arbeitsagentur.de/vamJB/stellenangeboteFinden.html;jsessionid=xTfJJgkZ1bpTtpGmQpLJtL12p3C22nv0b1PLwLqgd12DDwdtF5vy!-1460134633?execution=e1s1',
#    'Referer': 'http://jobboerse.arbeitsagentur.de/vamJB/stellenangeboteFinden.html;jsessionid=' + se.cookies['jsessionid'] + '?execution=e1s1',
    'Connection': 'keep-alive',
    'Pragma': 'no-cache',
    'Cache-Control': 'no-cache',
}

data = {
    '_eventId_stellenangeboteSuchen': 'Stellenangebote+suchen',
    'jb.flow.event.hauptfunktion': '_eventId_stellenangeboteSuchen',
    'allgemeineSuchkriterien.eingeklappt': 'false',
    'berufe.wert': '',
    '_keineAehnlicheBerufe.wert.value': 'on',
    'nurStellenMitFolgendenBegriffen.wert': 'Bio*',
    'suchbegriffebeziehung.wert.wert': '2',
    'nurStellenOhneFolgendeBegriffe.wert': '',
    'arbeitsort.plz.wert': '',
    'arbeitsort.ort.wert': 'Konstanz',
    'arbeitsort.region.wert.wert': 'leer',
    'umkreis.wert': '200',
    'stellenangeboteDerLetzten.wert.wert': '',
    'weitereSuchkriterien.eingeklappt': 'true',
    'fuhrungsverantwortung.wert.wert': '',
    'beginnDerTatigkeit.wert': '',
    '_arbeitszeitVollzeit.wert.value': 'on',
    '_arbeitszeitTeilzeitFlexibel.wert.value': 'on',
    '_arbeitszeitTeilzeitSchicht.wert.value': 'on',
    '_arbeitszeitTeilzeitVormittag.wert.value': 'on',
    '_arbeitszeitTeilzeitNachmittag.wert.value': 'on',
    '_arbeitszeitTeilzeitAbend.wert.value': 'on',
    '_arbeitszeitSchicht.wert.value': 'on',
    '_arbeitszeitNachtarbeit.wert.value': 'on',
    '_arbeitszeitWochenende.wert.value': 'on',
    '_arbeitszeitHeimarbeit.wert.value': 'on',
    'befristung.wert.wert': '',
    'geringfugigeBeschaftigungMiniJob.wert.wert': '',
    '_behinderung.wert.value': 'on',
    'betriebsgrosse.wert.wert': ''
}

resp3 = se.post('http://jobboerse.arbeitsagentur.de/vamJB/stellenangeboteFinden.html?execution=e1s1', headers=headers, cookies=cookies, data=data)



#
#try:
#    resp3a = resp3.history[0]
#    resp3b = resp3.history[1]
#    resp3c = resp3.history[2]
#except:
#    pass
#


#parseResultPage(resp3.text)






ddd = [tuple(_.split('=')) for _ in resp3.url.split('?')[1].split('&')]
e_str = ddd[0][1]
d_str = ddd[1][0][:-1]

page = 1

while page<10:
    print e_str, d_str, page, se.cookies['jsessionid']
   
    
    cookies = {
#        'expires': 'Sun, 15 Feb 2015 22:07:24 GMT',
#        'jsessionid': se.cookies['jsessionid'],
    }
    
    headers = {
        'Host': 'jobboerse.arbeitsagentur.de',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:31.0) Gecko/20100101 Firefox/31.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate',
    #    'Referer': 'http://jobboerse.arbeitsagentur.de/vamJB/stellenangeboteFinden.html?execution=e1s1&d_6827794_p=1',
        'Connection': 'keep-alive',
        'Pragma': 'no-cache',
        'Cache-Control': 'no-cache',
    }
    
    resp4 = se.get('http://jobboerse.arbeitsagentur.de/vamJB/stellenangeboteFinden.html?'+d_str+'z=50&execution='+e_str+'&'+d_str+'p='+str(page), headers=headers, cookies=cookies)

    success = parseResultPage(resp4.text)    
    
    time.sleep(2)
    
    if not success:
        page += 1
        continue
    
    tmp = bs(resp4.text).find_all(class_='fL')[1].text.strip().split()
    lw, hi = map(int, tmp[0].split('-'))
    mx = int(tmp[2])
    
    print lw, hi, mx, '\n'

    if hi<mx:
        page += 1
    else:
        break




for i, data in offers.items():

    print i, '%-40s' % data['title'][:40]

    adddata = {}
    if 'redirect_extern' not in data['link_jobdetails']:
        resp5 = se.get(data['link_jobdetails'])
        adddata = getJobDetails(resp5.text)
    print " >", len(adddata.keys())
    
    data['adddata'] = adddata
    data['description'] = adddata.get('Stellenbeschreibung', '---')

