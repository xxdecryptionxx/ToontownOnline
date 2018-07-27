# File: f (Python 2.4)

global _150_re, _227_re
import os
import sys

try:
    import SOCKS
    socket = SOCKS
    del SOCKS
    from socket import getfqdn
    socket.getfqdn = getfqdn
    del getfqdn
except ImportError:
    import socket

__all__ = [
    'FTP',
    'Netrc']
MSG_OOB = 1
FTP_PORT = 21

class Error(Exception):
    pass


class error_reply(Error):
    pass


class error_temp(Error):
    pass


class error_perm(Error):
    pass


class error_proto(Error):
    pass

all_errors = (Error, socket.error, IOError, EOFError)
CRLF = '\r\n'

class FTP:
    debugging = 0
    host = ''
    port = FTP_PORT
    sock = None
    file = None
    welcome = None
    passiveserver = 1
    
    def __init__(self, host = '', user = '', passwd = '', acct = ''):
        if host:
            self.connect(host)
            if user:
                self.login(user, passwd, acct)
            
        

    
    def connect(self, host = '', port = 0):
        if host:
            self.host = host
        
        if port:
            self.port = port
        
        msg = 'getaddrinfo returns an empty list'
        for res in socket.getaddrinfo(self.host, self.port, 0, socket.SOCK_STREAM):
            (af, socktype, proto, canonname, sa) = res
            
            try:
                self.sock = socket.socket(af, socktype, proto)
                self.sock.connect(sa)
            except socket.error:
                msg = None
                if self.sock:
                    self.sock.close()
                
                self.sock = None
                continue

            break
        
        if not self.sock:
            raise socket.error, msg
        
        self.af = af
        self.file = self.sock.makefile('rb')
        self.welcome = self.getresp()
        return self.welcome

    
    def getwelcome(self):
        if self.debugging:
            print '*welcome*', self.sanitize(self.welcome)
        
        return self.welcome

    
    def set_debuglevel(self, level):
        self.debugging = level

    debug = set_debuglevel
    
    def set_pasv(self, val):
        self.passiveserver = val

    
    def sanitize(self, s):
        if s[:5] == 'pass ' or s[:5] == 'PASS ':
            i = len(s)
            while i > 5 and s[i - 1] in '\r\n':
                i = i - 1
            s = s[:5] + '*' * (i - 5) + s[i:]
        
        return repr(s)

    
    def putline(self, line):
        line = line + CRLF
        if self.debugging > 1:
            print '*put*', self.sanitize(line)
        
        self.sock.sendall(line)

    
    def putcmd(self, line):
        if self.debugging:
            print '*cmd*', self.sanitize(line)
        
        self.putline(line)

    
    def getline(self):
        line = self.file.readline()
        if self.debugging > 1:
            print '*get*', self.sanitize(line)
        
        if not line:
            raise EOFError
        
        if line[-2:] == CRLF:
            line = line[:-2]
        elif line[-1:] in CRLF:
            line = line[:-1]
        
        return line

    
    def getmultiline(self):
        line = self.getline()
        if line[3:4] == '-':
            code = line[:3]
            while None:
                nextline = self.getline()
                line = line + '\n' + nextline
                if nextline[:3] == code and nextline[3:4] != '-':
                    break
                    continue
        
        return line

    
    def getresp(self):
        resp = self.getmultiline()
        if self.debugging:
            print '*resp*', self.sanitize(resp)
        
        self.lastresp = resp[:3]
        c = resp[:1]
        if c == '4':
            raise error_temp, resp
        
        if c == '5':
            raise error_perm, resp
        
        if c not in '123':
            raise error_proto, resp
        
        return resp

    
    def voidresp(self):
        resp = self.getresp()
        if resp[0] != '2':
            raise error_reply, resp
        
        return resp

    
    def abort(self):
        line = 'ABOR' + CRLF
        if self.debugging > 1:
            print '*put urgent*', self.sanitize(line)
        
        self.sock.sendall(line, MSG_OOB)
        resp = self.getmultiline()
        if resp[:3] not in ('426', '226'):
            raise error_proto, resp
        

    
    def sendcmd(self, cmd):
        self.putcmd(cmd)
        return self.getresp()

    
    def voidcmd(self, cmd):
        self.putcmd(cmd)
        return self.voidresp()

    
    def sendport(self, host, port):
        hbytes = host.split('.')
        pbytes = [
            repr(port / 256),
            repr(port % 256)]
        bytes = hbytes + pbytes
        cmd = 'PORT ' + ','.join(bytes)
        return self.voidcmd(cmd)

    
    def sendeprt(self, host, port):
        af = 0
        if self.af == socket.AF_INET:
            af = 1
        
        if self.af == socket.AF_INET6:
            af = 2
        
        if af == 0:
            raise error_proto, 'unsupported address family'
        
        fields = [
            '',
            repr(af),
            host,
            repr(port),
            '']
        cmd = 'EPRT ' + '|'.join(fields)
        return self.voidcmd(cmd)

    
    def makeport(self):
        msg = 'getaddrinfo returns an empty list'
        sock = None
        for res in socket.getaddrinfo(None, 0, self.af, socket.SOCK_STREAM, 0, socket.AI_PASSIVE):
            (af, socktype, proto, canonname, sa) = res
            
            try:
                sock = socket.socket(af, socktype, proto)
                sock.bind(sa)
            except socket.error:
                msg = None
                if sock:
                    sock.close()
                
                sock = None
                continue

            break
        
        if not sock:
            raise socket.error, msg
        
        sock.listen(1)
        port = sock.getsockname()[1]
        host = self.sock.getsockname()[0]
        if self.af == socket.AF_INET:
            resp = self.sendport(host, port)
        else:
            resp = self.sendeprt(host, port)
        return sock

    
    def makepasv(self):
        if self.af == socket.AF_INET:
            (host, port) = parse227(self.sendcmd('PASV'))
        else:
            (host, port) = parse229(self.sendcmd('EPSV'), self.sock.getpeername())
        return (host, port)

    
    def ntransfercmd(self, cmd, rest = None):
        size = None
        if self.passiveserver:
            (host, port) = self.makepasv()
            (af, socktype, proto, canon, sa) = socket.getaddrinfo(host, port, 0, socket.SOCK_STREAM)[0]
            conn = socket.socket(af, socktype, proto)
            conn.connect(sa)
            if rest is not None:
                self.sendcmd('REST %s' % rest)
            
            resp = self.sendcmd(cmd)
            if resp[0] != '1':
                raise error_reply, resp
            
        else:
            sock = self.makeport()
            if rest is not None:
                self.sendcmd('REST %s' % rest)
            
            resp = self.sendcmd(cmd)
            if resp[0] != '1':
                raise error_reply, resp
            
            (conn, sockaddr) = sock.accept()
        if resp[:3] == '150':
            size = parse150(resp)
        
        return (conn, size)

    
    def transfercmd(self, cmd, rest = None):
        return self.ntransfercmd(cmd, rest)[0]

    
    def login(self, user = '', passwd = '', acct = ''):
        if not user:
            user = 'anonymous'
        
        if not passwd:
            passwd = ''
        
        if not acct:
            acct = ''
        
        if user == 'anonymous' and passwd in ('', '-'):
            passwd = passwd + 'anonymous@'
        
        resp = self.sendcmd('USER ' + user)
        if resp[0] == '3':
            resp = self.sendcmd('PASS ' + passwd)
        
        if resp[0] == '3':
            resp = self.sendcmd('ACCT ' + acct)
        
        if resp[0] != '2':
            raise error_reply, resp
        
        return resp

    
    def retrbinary(self, cmd, callback, blocksize = 8192, rest = None):
        self.voidcmd('TYPE I')
        conn = self.transfercmd(cmd, rest)
        while None:
            data = conn.recv(blocksize)
            if not data:
                break
            
        conn.close()
        return self.voidresp()

    
    def retrlines(self, cmd, callback = None):
        if callback is None:
            callback = print_line
        
        resp = self.sendcmd('TYPE A')
        conn = self.transfercmd(cmd)
        fp = conn.makefile('rb')
        while None:
            line = fp.readline()
            if self.debugging > 2:
                print '*retr*', repr(line)
            
            if not line:
                break
            
            if line[-2:] == CRLF:
                line = line[:-2]
            elif line[-1:] == '\n':
                line = line[:-1]
            
        fp.close()
        conn.close()
        return self.voidresp()

    
    def storbinary(self, cmd, fp, blocksize = 8192):
        self.voidcmd('TYPE I')
        conn = self.transfercmd(cmd)
        while None:
            buf = fp.read(blocksize)
            if not buf:
                break
            
        conn.close()
        return self.voidresp()

    
    def storlines(self, cmd, fp):
        self.voidcmd('TYPE A')
        conn = self.transfercmd(cmd)
        while None:
            buf = fp.readline()
            if not buf:
                break
            
            if buf[-2:] != CRLF:
                if buf[-1] in CRLF:
                    buf = buf[:-1]
                
                buf = buf + CRLF
            
        conn.close()
        return self.voidresp()

    
    def acct(self, password):
        cmd = 'ACCT ' + password
        return self.voidcmd(cmd)

    
    def nlst(self, *args):
        cmd = 'NLST'
        for arg in args:
            cmd = cmd + ' ' + arg
        
        files = []
        self.retrlines(cmd, files.append)
        return files

    
    def dir(self, *args):
        cmd = 'LIST'
        func = None
        if args[-1:] and type(args[-1]) != type(''):
            args = args[:-1]
            func = args[-1]
        
        for arg in args:
            if arg:
                cmd = cmd + ' ' + arg
                continue
        
        self.retrlines(cmd, func)

    
    def rename(self, fromname, toname):
        resp = self.sendcmd('RNFR ' + fromname)
        if resp[0] != '3':
            raise error_reply, resp
        
        return self.voidcmd('RNTO ' + toname)

    
    def delete(self, filename):
        resp = self.sendcmd('DELE ' + filename)
        if resp[:3] in ('250', '200'):
            return resp
        elif resp[:1] == '5':
            raise error_perm, resp
        else:
            raise error_reply, resp

    
    def cwd(self, dirname):
        if dirname == '..':
            
            try:
                return self.voidcmd('CDUP')
            except error_perm:
                msg = None
                if msg.args[0][:3] != '500':
                    raise 
                
            except:
                msg.args[0][:3] != '500'
            

        if dirname == '':
            dirname = '.'
        
        cmd = 'CWD ' + dirname
        return self.voidcmd(cmd)

    
    def size(self, filename):
        resp = self.sendcmd('SIZE ' + filename)
        if resp[:3] == '213':
            s = resp[3:].strip()
            
            try:
                return int(s)
            except (OverflowError, ValueError):
                return long(s)
            


    
    def mkd(self, dirname):
        resp = self.sendcmd('MKD ' + dirname)
        return parse257(resp)

    
    def rmd(self, dirname):
        return self.voidcmd('RMD ' + dirname)

    
    def pwd(self):
        resp = self.sendcmd('PWD')
        return parse257(resp)

    
    def quit(self):
        resp = self.voidcmd('QUIT')
        self.close()
        return resp

    
    def close(self):
        if self.file:
            self.file.close()
            self.sock.close()
            self.file = None
            self.sock = None
        


_150_re = None

def parse150(resp):
    global _150_re
    if resp[:3] != '150':
        raise error_reply, resp
    
    if _150_re is None:
        import re as re
        _150_re = re.compile('150 .* \\((\\d+) bytes\\)', re.IGNORECASE)
    
    m = _150_re.match(resp)
    if not m:
        return None
    
    s = m.group(1)
    
    try:
        return int(s)
    except (OverflowError, ValueError):
        return long(s)


_227_re = None

def parse227(resp):
    global _227_re
    if resp[:3] != '227':
        raise error_reply, resp
    
    if _227_re is None:
        import re
        _227_re = re.compile('(\\d+),(\\d+),(\\d+),(\\d+),(\\d+),(\\d+)')
    
    m = _227_re.search(resp)
    if not m:
        raise error_proto, resp
    
    numbers = m.groups()
    host = '.'.join(numbers[:4])
    port = (int(numbers[4]) << 8) + int(numbers[5])
    return (host, port)


def parse229(resp, peer):
    if resp[:3] != '229':
        raise error_reply, resp
    
    left = resp.find('(')
    if left < 0:
        raise error_proto, resp
    
    right = resp.find(')', left + 1)
    if right < 0:
        raise error_proto, resp
    
    if resp[left + 1] != resp[right - 1]:
        raise error_proto, resp
    
    parts = resp[left + 1:right].split(resp[left + 1])
    if len(parts) != 5:
        raise error_proto, resp
    
    host = peer[0]
    port = int(parts[3])
    return (host, port)


def parse257(resp):
    if resp[:3] != '257':
        raise error_reply, resp
    
    if resp[3:5] != ' "':
        return ''
    
    dirname = ''
    i = 5
    n = len(resp)
    while i < n:
        c = resp[i]
        i = i + 1
        if c == '"':
            if i >= n or resp[i] != '"':
                break
            
            i = i + 1
        
        dirname = dirname + c
    return dirname


def print_line(line):
    print line


def ftpcp(source, sourcename, target, targetname = '', type = 'I'):
    if not targetname:
        targetname = sourcename
    
    type = 'TYPE ' + type
    source.voidcmd(type)
    target.voidcmd(type)
    (sourcehost, sourceport) = parse227(source.sendcmd('PASV'))
    target.sendport(sourcehost, sourceport)
    treply = target.sendcmd('STOR ' + targetname)
    if treply[:3] not in ('125', '150'):
        raise error_proto
    
    sreply = source.sendcmd('RETR ' + sourcename)
    if sreply[:3] not in ('125', '150'):
        raise error_proto
    
    source.voidresp()
    target.voidresp()


class Netrc:
    _Netrc__defuser = None
    _Netrc__defpasswd = None
    _Netrc__defacct = None
    
    def __init__(self, filename = None):
        if filename is None:
            if 'HOME' in os.environ:
                filename = os.path.join(os.environ['HOME'], '.netrc')
            else:
                raise IOError, 'specify file to load or set $HOME'
        
        self._Netrc__hosts = { }
        self._Netrc__macros = { }
        fp = open(filename, 'r')
        in_macro = 0
        while None:
            line = fp.readline()
            if not line:
                break
            
            if in_macro and line.strip():
                macro_lines.append(line)
                continue
            elif in_macro:
                self._Netrc__macros[macro_name] = tuple(macro_lines)
                in_macro = 0
            
            words = line.split()
            host = None
            user = None
            passwd = None
            acct = None
            default = 0
            i = 0
            while i < len(words):
                w1 = words[i]
                if i + 1 < len(words):
                    w2 = words[i + 1]
                else:
                    w2 = None
                if w1 == 'default':
                    default = 1
                elif w1 == 'machine' and w2:
                    host = w2.lower()
                    i = i + 1
                elif w1 == 'login' and w2:
                    user = w2
                    i = i + 1
                elif w1 == 'password' and w2:
                    passwd = w2
                    i = i + 1
                elif w1 == 'account' and w2:
                    acct = w2
                    i = i + 1
                elif w1 == 'macdef' and w2:
                    macro_name = w2
                    macro_lines = []
                    in_macro = 1
                    break
                
                i = i + 1
            if default:
                if not user:
                    pass
                self._Netrc__defuser = self._Netrc__defuser
                if not passwd:
                    pass
                self._Netrc__defpasswd = self._Netrc__defpasswd
                if not acct:
                    pass
                self._Netrc__defacct = self._Netrc__defacct
            
            if host:
                if host in self._Netrc__hosts:
                    (ouser, opasswd, oacct) = self._Netrc__hosts[host]
                    if not user:
                        pass
                    user = ouser
                    if not passwd:
                        pass
                    passwd = opasswd
                    if not acct:
                        pass
                    acct = oacct
                
                self._Netrc__hosts[host] = (user, passwd, acct)
                continue
        fp.close()

    
    def get_hosts(self):
        return self._Netrc__hosts.keys()

    
    def get_account(self, host):
        host = host.lower()
        user = None
        passwd = None
        acct = None
        if host in self._Netrc__hosts:
            (user, passwd, acct) = self._Netrc__hosts[host]
        
        if not user:
            pass
        user = self._Netrc__defuser
        if not passwd:
            pass
        passwd = self._Netrc__defpasswd
        if not acct:
            pass
        acct = self._Netrc__defacct
        return (user, passwd, acct)

    
    def get_macros(self):
        return self._Netrc__macros.keys()

    
    def get_macro(self, macro):
        return self._Netrc__macros[macro]



def test():
    debugging = 0
    rcfile = None
    while sys.argv[1] == '-d':
        debugging = debugging + 1
        del sys.argv[1]
    if sys.argv[1][:2] == '-r':
        rcfile = sys.argv[1][2:]
        del sys.argv[1]
    
    host = sys.argv[1]
    ftp = FTP(host)
    ftp.set_debuglevel(debugging)
    userid = ''
    passwd = ''
    acct = ''
    
    try:
        netrc = Netrc(rcfile)
    except IOError:
        if rcfile is not None:
            sys.stderr.write('Could not open account file -- using anonymous login.')
        
    except:
        rcfile is not None

    
    try:
        (userid, passwd, acct) = netrc.get_account(host)
    except KeyError:
        sys.stderr.write('No account -- using anonymous login.')

    ftp.login(userid, passwd, acct)
    for file in sys.argv[2:]:
        if file[:2] == '-l':
            ftp.dir(file[2:])
            continue
        if file[:2] == '-d':
            cmd = 'CWD'
            if file[2:]:
                cmd = cmd + ' ' + file[2:]
            
            resp = ftp.sendcmd(cmd)
            continue
        if file == '-p':
            ftp.set_pasv(not (ftp.passiveserver))
            continue
        ftp.retrbinary('RETR ' + file, sys.stdout.write, 1024)
    
    ftp.quit()

if __name__ == '__main__':
    test()

