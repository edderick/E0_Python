import urllib2
import urllib
import web
import bitstring
import StateMachine
import main

amMaster = False


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
    return main.ID < main.otherID

class Kc:
  def POST(self):
    data = web.input()
    main.kcPrime = Bits(hex=data.Kc)
    return 1

class Message:
  def POST(self):
    data = web.input()
    plaintext = Bits(bytes=data.plaintext)
    main.clock = Bits(uint=main.clock.uint + 1, length=26)
     
    keystream,ciphertext = StateMachine.encipher(main.masterID, main.kcPrime,
    main.clock, plaintext)
    main.conn.send_data(clock.uint, ciphertext.bytes)

    main.send_log()
    
    return 1


def start_server(globals):
  if __name__ == '__main__':
    app = web.application(urls, globals())
    app.run()

