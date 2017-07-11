# File: e (Python 2.4)

import base64
from quopri import encodestring as _encodestring

def _qencode(s):
    enc = _encodestring(s, quotetabs = True)
    return enc.replace(' ', '=20')


def _bencode(s):
    if not s:
        return s
    
    hasnewline = s[-1] == '\n'
    value = base64.encodestring(s)
    if not hasnewline and value[-1] == '\n':
        return value[:-1]
    
    return value


def encode_base64(msg):
    orig = msg.get_payload()
    encdata = _bencode(orig)
    msg.set_payload(encdata)
    msg['Content-Transfer-Encoding'] = 'base64'


def encode_quopri(msg):
    orig = msg.get_payload()
    encdata = _qencode(orig)
    msg.set_payload(encdata)
    msg['Content-Transfer-Encoding'] = 'quoted-printable'


def encode_7or8bit(msg):
    orig = msg.get_payload()
    if orig is None:
        msg['Content-Transfer-Encoding'] = '7bit'
        return None
    
    
    try:
        orig.encode('ascii')
    except UnicodeError:
        charset = msg.get_charset()
        if charset:
            pass
        output_cset = charset.output_charset
        if output_cset and output_cset.lower().startswith('iso-2202-'):
            msg['Content-Transfer-Encoding'] = '7bit'
        else:
            msg['Content-Transfer-Encoding'] = '8bit'
    except:
        output_cset.lower().startswith('iso-2202-')

    msg['Content-Transfer-Encoding'] = '7bit'


def encode_noop(msg):
    pass

