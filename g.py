import base64
import Client
import datetime
def send_log(recieving, master, keystream, ciphertext, plaintext):
     d = datetime.now()
	   vals = {
	   "CLK" : clock.uint,
	   "BD_ADDR" : ID.hex,
	   "is_receiving" : recieving,
	   "keystream" : base64.b64encode(keystream.bytes),
	   "ciphertext" : base64.b64encode(ciphertext.bytes),
	   "plaintext" : plaintext.bytes,
	   "timestamp" : d.strftime("[%b %d %H:%M:%S]") }

	   Client.postTo('localhost', '8000', 'log', vals, 'POST', 'master' if master else 'slave')
