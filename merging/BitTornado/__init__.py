product_name = 'ABC'
version_short = 'ABC-3.1.0'

version = version_short + ' (' + product_name + ' - BitTornado 0.3.13'
report_email = version_short+'@degreez.net'

from types import StringType
from sha import sha
from time import time, clock
from string import strip
import socket
try:
    from os import getpid
except ImportError:
    def getpid():
        return 1
import permid
import cachedb2
from base64 import decodestring 
    
mapbase64 = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz.-'

def read_pubkey(filename):
    try:
        file = open(filename, "r")
    except:
        raise RuntimeError, "Cannot open " + filename + " to read my PermID. Abort"
    lines= file.readlines()
    pubkey = ''
    for line in lines:
        if line.startswith('-----BEGIN PUBLIC KEY-----'):
            pubkey = ''
        elif line.startswith('-----END PUBLIC KEY-----'):
            break
        else:
            pubkey += strip(line)
    return pubkey

def is_valid_ip(ip):
    invalid_iphead = ['0.', '127.0.0.1']
    for iphead in invalid_iphead:
        if ip.startswith(iphead):
            return False
    return True

def load_myinfo():    # TODO: load more personal infomation
    my_permid64 = read_pubkey('ecpub.pem')
    my_permid = decodestring(my_permid64)
    name = socket.gethostname()
    host = socket.gethostbyname_ex(name)
    ipaddrlist = host[2]
    valid_ip = ''
    for ip in ipaddrlist:
        if is_valid_ip(ip):
            valid_ip = ip
            break
    myinfo = {'permid':my_permid, 'ip':valid_ip, 'name':name}
    return myinfo
    
_idprefix = version_short[0]
#for subver in version_short[2:].split('.'):
for subver in version_short.split('-')[1].split('.'):
    try:
        subver = int(subver)
    except:
        subver = 0
    _idprefix += mapbase64[subver]
_idprefix += ('-' * (6-len(_idprefix)))
_idrandom = [None]
permid.init()
myinfo = load_myinfo()
cachedb2.init(myinfo)

def resetPeerIDs():
    try:
        f = open('/dev/urandom', 'rb')
        x = f.read(20)
        f.close()
    except:
        x = ''

    l1 = 0
    t = clock()
    while t == clock():
        l1 += 1
    l2 = 0
    t = long(time()*100)
    while t == long(time()*100):
        l2 += 1
    l3 = 0
    if l2 < 1000:
        t = long(time()*10)
        while t == long(clock()*10):
            l3 += 1
    x += ( repr(time()) + '/' + str(time()) + '/'
           + str(l1) + '/' + str(l2) + '/' + str(l3) + '/'
           + str(getpid()) )

    s = ''
    for i in sha(x).digest()[-11:]:
        s += mapbase64[ord(i) & 0x3F]
    _idrandom[0] = s
        
resetPeerIDs()

def createPeerID(ins = '---'):
    assert type(ins) is StringType
    assert len(ins) == 3
    return _idprefix + ins + _idrandom[0]
