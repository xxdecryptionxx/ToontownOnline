# File: w (Python 2.4)

import os
import sys
__all__ = [
    'Error',
    'open',
    'get',
    'register']

class Error(Exception):
    pass

_browsers = { }
_tryorder = []

def register(name, klass, instance = None):
    _browsers[name.lower()] = [
        klass,
        instance]


def get(using = None):
    if using is not None:
        alternatives = [
            using]
    else:
        alternatives = _tryorder
    for browser in alternatives:
        if '%s' in browser:
            return GenericBrowser(browser)
            continue
        
        try:
            command = _browsers[browser.lower()]
        except KeyError:
            command = _synthesize(browser)

        if command[1] is None:
            return command[0]()
            continue
        return command[1]
    
    raise Error('could not locate runnable browser')


def open(url, new = 0, autoraise = 1):
    get().open(url, new, autoraise)


def open_new(url):
    get().open(url, 1)


def _synthesize(browser):
    if not os.path.exists(browser):
        return [
            None,
            None]
    
    name = os.path.basename(browser)
    
    try:
        command = _browsers[name.lower()]
    except KeyError:
        return [
            None,
            None]

    controller = command[1]
    if controller and name.lower() == controller.basename:
        import copy as copy
        controller = copy.copy(controller)
        controller.name = browser
        controller.basename = os.path.basename(browser)
        register(browser, None, controller)
        return [
            None,
            controller]
    
    return [
        None,
        None]


def _iscommand(cmd):
    path = os.environ.get('PATH')
    if not path:
        return False
    
    for d in path.split(os.pathsep):
        exe = os.path.join(d, cmd)
        if os.path.isfile(exe):
            return True
            continue
    
    return False

PROCESS_CREATION_DELAY = 4

class GenericBrowser:
    
    def __init__(self, cmd):
        (self.name, self.args) = cmd.split(None, 1)
        self.basename = os.path.basename(self.name)

    
    def open(self, url, new = 0, autoraise = 1):
        command = '%s %s' % (self.name, self.args)
        os.system(command % url)

    
    def open_new(self, url):
        self.open(url)



class Netscape:
    
    def __init__(self, name):
        self.name = name
        self.basename = os.path.basename(name)

    
    def _remote(self, action, autoraise):
        raise_opt = ('-noraise', '-raise')[autoraise]
        cmd = "%s %s -remote '%s' >/dev/null 2>&1" % (self.name, raise_opt, action)
        rc = os.system(cmd)
        if rc:
            import time as time
            os.system('%s &' % self.name)
            time.sleep(PROCESS_CREATION_DELAY)
            rc = os.system(cmd)
        
        return not rc

    
    def open(self, url, new = 0, autoraise = 1):
        if new:
            self._remote('openURL(%s, new-window)' % url, autoraise)
        else:
            self._remote('openURL(%s)' % url, autoraise)

    
    def open_new(self, url):
        self.open(url, 1)



class Galeon:
    
    def __init__(self, name):
        self.name = name
        self.basename = os.path.basename(name)

    
    def _remote(self, action, autoraise):
        raise_opt = ('--noraise', '')[autoraise]
        cmd = '%s %s %s >/dev/null 2>&1' % (self.name, raise_opt, action)
        rc = os.system(cmd)
        if rc:
            import time
            os.system('%s >/dev/null 2>&1 &' % self.name)
            time.sleep(PROCESS_CREATION_DELAY)
            rc = os.system(cmd)
        
        return not rc

    
    def open(self, url, new = 0, autoraise = 1):
        if new:
            self._remote("-w '%s'" % url, autoraise)
        else:
            self._remote("-n '%s'" % url, autoraise)

    
    def open_new(self, url):
        self.open(url, 1)



class Konqueror:
    
    def __init__(self):
        if _iscommand('konqueror'):
            self.name = 'konqueror'
            self.basename = 'konqueror'
        else:
            self.name = 'kfm'
            self.basename = 'kfm'

    
    def _remote(self, action):
        cmd = 'kfmclient %s >/dev/null 2>&1' % action
        rc = os.system(cmd)
        if rc:
            import time
            if self.basename == 'konqueror':
                os.system(self.name + ' --silent &')
            else:
                os.system(self.name + ' -d &')
            time.sleep(PROCESS_CREATION_DELAY)
            rc = os.system(cmd)
        
        return not rc

    
    def open(self, url, new = 1, autoraise = 1):
        self._remote("openURL '%s'" % url)

    open_new = open


class Grail:
    
    def _find_grail_rc(self):
        import glob as glob
        import pwd as pwd
        import socket as socket
        import tempfile as tempfile
        tempdir = os.path.join(tempfile.gettempdir(), '.grail-unix')
        user = pwd.getpwuid(os.getuid())[0]
        filename = os.path.join(tempdir, user + '-*')
        maybes = glob.glob(filename)
        if not maybes:
            return None
        
        s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        for fn in maybes:
            
            try:
                s.connect(fn)
            except socket.error:
                
                try:
                    os.unlink(fn)
                except IOError:
                    pass
                


            return s
        

    
    def _remote(self, action):
        s = self._find_grail_rc()
        if not s:
            return 0
        
        s.send(action)
        s.close()
        return 1

    
    def open(self, url, new = 0, autoraise = 1):
        if new:
            self._remote('LOADNEW ' + url)
        else:
            self._remote('LOAD ' + url)

    
    def open_new(self, url):
        self.open(url, 1)



class WindowsDefault:
    
    def open(self, url, new = 0, autoraise = 1):
        os.startfile(url)

    
    def open_new(self, url):
        self.open(url)


if os.environ.get('TERM') or os.environ.get('DISPLAY'):
    _tryorder = [
        'links',
        'lynx',
        'w3m']
    if os.environ.get('TERM'):
        if _iscommand('links'):
            register('links', None, GenericBrowser("links '%s'"))
        
        if _iscommand('lynx'):
            register('lynx', None, GenericBrowser("lynx '%s'"))
        
        if _iscommand('w3m'):
            register('w3m', None, GenericBrowser("w3m '%s'"))
        
    
    if os.environ.get('DISPLAY'):
        _tryorder = [
            'galeon',
            'skipstone',
            'mozilla-firefox',
            'mozilla-firebird',
            'mozilla',
            'netscape',
            'kfm',
            'grail'] + _tryorder
        for browser in ('mozilla-firefox', 'mozilla-firebird', 'mozilla', 'netscape'):
            if _iscommand(browser):
                register(browser, None, Netscape(browser))
                continue
        
        if _iscommand('mosaic'):
            register('mosaic', None, GenericBrowser("mosaic '%s' >/dev/null &"))
        
        if _iscommand('galeon'):
            register('galeon', None, Galeon('galeon'))
        
        if _iscommand('skipstone'):
            register('skipstone', None, GenericBrowser("skipstone '%s' >/dev/null &"))
        
        if _iscommand('kfm') or _iscommand('konqueror'):
            register('kfm', Konqueror, Konqueror())
        
        if _iscommand('grail'):
            register('grail', Grail, None)
        
    


class InternetConfig:
    
    def open(self, url, new = 0, autoraise = 1):
        ic.launchurl(url)

    
    def open_new(self, url):
        self.open(url)


if sys.platform[:3] == 'win':
    _tryorder = [
        'netscape',
        'windows-default']
    register('windows-default', WindowsDefault)


try:
    import ic
except ImportError:
    pass

_tryorder = [
    'internet-config']
register('internet-config', InternetConfig)
if sys.platform[:3] == 'os2' and _iscommand('netscape.exe'):
    _tryorder = [
        'os2netscape']
    register('os2netscape', None, GenericBrowser('start netscape.exe %s'))

if 'BROWSER' in os.environ:
    _tryorder = os.environ['BROWSER'].split(os.pathsep)

for cmd in _tryorder:
    if cmd.lower() not in _browsers:
        if _iscommand(cmd.lower()):
            register(cmd.lower(), None, GenericBrowser("%s '%%s'" % cmd.lower()))
        
    _iscommand(cmd.lower())

cmd = None
del cmd
_tryorder = filter(lambda x: if not x.lower() in _browsers:
passx.find('%s') > -1, _tryorder)
