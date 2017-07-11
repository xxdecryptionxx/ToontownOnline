# File: e (Python 2.4)

import codecs
encode = codecs.utf_8_encode

def decode(input, errors = 'strict'):
    return codecs.utf_8_decode(input, errors, True)


class StreamWriter(codecs.StreamWriter):
    encode = codecs.utf_8_encode


class StreamReader(codecs.StreamReader):
    decode = codecs.utf_8_decode


def getregentry():
    return (encode, decode, StreamReader, StreamWriter)

