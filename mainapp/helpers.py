# -*- coding: utf-8 -*-
"""
Created on Sun Feb 15 13:12:05 2015

@author: rafik
"""

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