# -*- coding: utf-8 -*-
"""
intended to be %run with ipython..

Created on Sun Feb 15 13:12:05 2015

@author: rafik
"""

log = []
offers = {}

import os
import webbrowser
import tempfile



def showHTML(html, isBody=False):
    
    if isBody:
        html = '<html><head></head><body>\n\n' + html + '\n\n</body></html>'
    
#    fobj, fpath = tempfile.mkstemp(suffix='.html', prefix='showHTML__', text=True)
    
    with tempfile.NamedTemporaryFile(suffix='.html', prefix='showHTML__', delete=False) as fobj:
        url = 'file://' + fobj.name
        
        fobj.write(html.encode('utf8'))
        fobj.flush()
        webbrowser.open(url)
        
def printlog():
    for l in log:
        print l
        
def printres():
    for k, data in sorted(offers.items()):
        print '%03i | %-30s | %-40s' % (k, data['title'][:30], data['description'][:40])
