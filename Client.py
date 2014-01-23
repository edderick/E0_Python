import urllib2
import urllib
import web
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
    print 'recieved isMaster request'
    return g.ID == g.masterID

class Kc:
  def POST(self):
    data = web.input()
    g.kcPrime = Bits(hex=data.Kc)
    print 'recieved Kc request'
    return 1

class Message:
  def POST(self):
    print 'recieved message request'
    data = web.input()
    plaintext = Bits(bytes=data.plaintext.encode('utf-8'))
    g.clock = Bits(uint=g.clock.uint + 1, length=26)
     
    keystream,ciphertext =StateMachine.encipher(g.masterID, g.kcPrime,
    g.clock, plaintext)
    g.conn.send_data(g.clock.uint, ciphertext.bytes)

    g.send_log(False, g.ID == g.masterID, keystream, ciphertext, plaintext)
    
    return 1


class MyApplication(web.application):
	def run(self, port=8888, *middleware):
		func = self.wsgifunc(*middleware)
        	return web.httpserver.runsimple(func, ('0.0.0.0', port))
def start_server():
  #if __name__ == '__main__':
    app = MyApplication(urls, globals())
    print 'HTTP client started'
    app.run(port=g.httpPort)
    
