import urllib2
import urllib
import web
import threading
from bitstring import *
import StateMachine
import main
import g


def postTo(domain,port,slug, vals, method, role):
    protocol = 'http'
    url = protocol + '://' + domain + ':' + port + '/' + slug
    rolequery = 'role=' + role
    
    data = urllib.urlencode(vals)
    req = urllib2.Request(url + '?' + rolequery, data)
    response = urllib2.urlopen(req)
    
    return response.read()
        
urls = ('/Kc', 'Kc','/isMaster', 'isMaster', '/message', 'Message')

class isMaster:
  def GET(self):
    print 'recieved isMaster request, will return ', g.ID ==g.masterID
    return g.ID == g.masterID

class Kc:
  def POST(self):
    data = web.input()
    g.kcPrime = Bits(hex=data.Kc)
    print 'recieved Kc request, set KcPrime to:', g.kcPrime
    return 1

class Message:
  def POST(self):
    print 'recieved message request'
    data = web.input()
    plaintext = Bits(bytes=data.plaintext.encode('utf-8')) 
    rev = BitArray(g.clock)
    rev.reverse()
    keystream,ciphertext =StateMachine.encipher(g.masterID, g.kcPrime,
    rev, plaintext)
    print "Sending forward Data"
    g.conn.send_data(g.clock.uint, ciphertext.bytes)

    g.send_log(False, g.ID == g.masterID, keystream, ciphertext, plaintext)
    
    return 1


class MyApplication(web.application):
	def run(self, port=8888, *middleware):
		func = self.wsgifunc(*middleware)
        	return web.httpserver.runsimple(func, ('0.0.0.0', port))


class MyWebServer(threading.Thread):
 def run(self):
    #if __name__ == '__main__':
    app = MyApplication(urls, globals())
    print 'HTTP client started'
    app.run(port=g.httpPort)
    

