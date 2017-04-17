
import pycurl
from StringIO import StringIO

str = "TIPI.TCP=192.168.1.144:9902"

print str.split("=")[1].split(":")

CHUNKSIZE = 3

def __splitMessage(bytes):
    l = len(bytes)
    chunks = [ ]
    bc = (l / CHUNKSIZE) + 1
    for i in range(bc):
	chunk = bytes[i*CHUNKSIZE:(i+1)*CHUNKSIZE]
	if len(chunk):
	    chunks += [ chunk ]
    return chunks


print __splitMessage(bytearray("1234"))

#

buffer = StringIO()
c = pycurl.Curl()
c.setopt(c.URL, 'http://ti994a.cwfk.net/')
c.setopt(c.WRITEDATA, buffer)
c.perform()
c.close()

body = buffer.getvalue()

print(body)

