import base64
import Client
def send_log(recieving, master, keystream, ciphertext, plaintext):
	   vals = {
	   "CLK" : clock.uint,
	   "BD_ADDR" : ID.hex,
	   "is_recieving" : recieving,
	   "keystream" : base64.b64encode(keystream.bytes),
	   "ciphertext" : base64.b64encode(ciphertext.bytes),
	   "plaintext" : plaintext.bytes,
	   "timestamp" : '22nd janudary' }

	   Client.postTo('localhost', '8000', 'log', vals, 'POST', 'master' if master else 'slave')