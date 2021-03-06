#!/usr/bin/python
"""

$Id$

Crawler"""


import llyn
from term import Fragment
#import thing
import diag

import sys

from myStore import load, symbol
from uripath import join, base

cvsRevision = "$Revision$"

document = {}
already = []
agenda = []
successes = 0

class Document:
    def __init__(self, x):
	self.item = x
	self.mentions = []

def getDoc(r):
    d = document.get(r, None)
    if d != None: return d
    d = Document(r)
    document[r] = d
    return d
	
def crawl(this):
    global agenda
    global already
    global successes
    uri = this.uriref()
    print
    print "<%s> a" % uri,
    try:
	f = load(uri)
    except:
	print ":Inaccessible."
	return
    print ":Accessible",
    successes = successes + 1
    thisd = getDoc(this)
    for s in f.statements:
	for p in 1,2,3:
	    x = s[p]
	    if isinstance(x, Fragment):
		r = x.resource
		if r not in thisd.mentions:
		    thisd.mentions.append(r)
		    print   ";\n\t:mentionsSomethingIn <%s>" % r.uriref(),
		    if r not in agenda and r not in already:
			agenda.append(r)
    print "."
	    

    
def doCommand():
    """Command line RDF/N3 crawler
        
 crawl <uriref>

options:
 
See http://www.w3.org/2000/10/swap/doc/cwm  for more documentation.
"""
    global agenda
    global already
    uriref = sys.argv[1]
    uri = join(base(), uriref)
    r = symbol(uri)
    diag.setVerbosity(0)
    print "@prefix : <http://www.w3.org/2000/10/swap/util/semweb#>."
    print "# Generated by crawl.py ", cvsRevision[1:-1]
    agenda = [r]
    while agenda != []:
	r = agenda[0]
	agenda = agenda[1:]
	already.append(r)
	crawl(r)
    print "# ", len(already), "attempts,", successes, "successes."

############################################################ Main program
    
if __name__ == '__main__':
    import os
    doCommand()

