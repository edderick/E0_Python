# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <markdowncell>

# #Test Posting Data to site

# <codecell>

import urllib2
import urllib

def postTo(domain,port,slug, vals, method, role):
    
    protocol = 'http'
    url = protocol + '://' + domain + ':' + port + '/' + slug
    rolequery = 'role=' + role
    
    data = urllib.urlencode(vals)
    
    
    if(method == 'get'):
        print 'method: get'
        req = urllib2.Request(url + '?' + rolequery + '&' +  data)
    elif(method == 'post'):
        print 'method: post'
        req = urllib2.Request(url + '?' + rolequery, data)
    else:
        print 'bad method'
    response = urllib2.urlopen(req)
    
    print url + '?' + rolequery + '&' + data
    print response.read()
        

vals  = {
 'content' : 'some',
'msg' : 'rand'}

domain = 'localhost'
port = '8000'
slug = 'keyStream'

postTo(domain, port, slug, vals, 'post', 'slave')


# <codecell>


# <codecell>


# <codecell>


