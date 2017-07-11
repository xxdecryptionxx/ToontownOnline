# File: s (Python 2.4)

import sys
import os
import __builtin__

def makepath(*paths):
    dir = os.path.abspath(os.path.join(*paths))
    return (dir, os.path.normcase(dir))


def abs__file__():
    for m in sys.modules.values():
        
        try:
            m.__file__ = os.path.abspath(m.__file__)
        continue
        except AttributeError:
            continue
            continue
        

    


def removeduppaths():
    L = []
    known_paths = set()
    for dir in sys.path:
        (dir, dircase) = makepath(dir)
        if dircase not in known_paths:
            L.append(dir)
            known_paths.add(dircase)
            continue
    
    sys.path[:] = L
    return known_paths


def addbuilddir():
    get_platform = get_platform
    import distutils.util
    s = 'build/lib.%s-%.3s' % (get_platform(), sys.version)
    s = os.path.join(os.path.dirname(sys.path[-1]), s)
    sys.path.append(s)


def _init_pathinfo():
    d = set()
    for dir in sys.path:
        
        try:
            if os.path.isdir(dir):
                (dir, dircase) = makepath(dir)
                d.add(dircase)
        continue
        except TypeError:
            continue
            continue
        

    
    return d


def addpackage(sitedir, name, known_paths):
    if known_paths is None:
        _init_pathinfo()
        reset = 1
    else:
        reset = 0
    fullname = os.path.join(sitedir, name)
    
    try:
        f = open(fullname, 'rU')
    except IOError:
        return None

    
    try:
        for line in f:
            if line.startswith('#'):
                continue
            
            if line.startswith('import'):
                exec line
                continue
            
            line = line.rstrip()
            (dir, dircase) = makepath(sitedir, line)
            if dircase not in known_paths and os.path.exists(dir):
                sys.path.append(dir)
                known_paths.add(dircase)
                continue
    finally:
        f.close()

    if reset:
        known_paths = None
    
    return known_paths


def addsitedir(sitedir, known_paths = None):
    if known_paths is None:
        known_paths = _init_pathinfo()
        reset = 1
    else:
        reset = 0
    (sitedir, sitedircase) = makepath(sitedir)
    if sitedircase not in known_paths:
        sys.path.append(sitedir)
    
    
    try:
        names = os.listdir(sitedir)
    except os.error:
        return None

    names.sort()
    for name in names:
        if name.endswith(os.extsep + 'pth'):
            addpackage(sitedir, name, known_paths)
            continue
    
    if reset:
        known_paths = None
    
    return known_paths


def addsitepackages(known_paths):
    prefixes = [
        sys.prefix]
    if sys.exec_prefix != sys.prefix:
        prefixes.append(sys.exec_prefix)
    
    for prefix in prefixes:
        if prefix:
            if sys.platform in ('os2emx', 'riscos'):
                sitedirs = [
                    os.path.join(prefix, 'Lib', 'site-packages')]
            elif os.sep == '/':
                sitedirs = [
                    os.path.join(prefix, 'lib', 'python' + sys.version[:3], 'site-packages'),
                    os.path.join(prefix, 'lib', 'site-python')]
            else:
                sitedirs = [
                    prefix,
                    os.path.join(prefix, 'lib', 'site-packages')]
            if sys.platform == 'darwin':
                if 'Python.framework' in prefix:
                    home = os.environ.get('HOME')
                    if home:
                        sitedirs.append(os.path.join(home, 'Library', 'Python', sys.version[:3], 'site-packages'))
                    
                
            
            for sitedir in sitedirs:
                if os.path.isdir(sitedir):
                    addsitedir(sitedir, known_paths)
                    continue
            
    


def setBEGINLIBPATH():
    dllpath = os.path.join(sys.prefix, 'Lib', 'lib-dynload')
    libpath = os.environ['BEGINLIBPATH'].split(';')
    if libpath[-1]:
        libpath.append(dllpath)
    else:
        libpath[-1] = dllpath
    os.environ['BEGINLIBPATH'] = ';'.join(libpath)


def setquit():
    if os.sep == ':':
        exit = 'Use Cmd-Q to quit.'
    elif os.sep == '\\':
        exit = 'Use Ctrl-Z plus Return to exit.'
    else:
        exit = 'Use Ctrl-D (i.e. EOF) to exit.'
    __builtin__.quit = exit
    __builtin__.exit = exit


class _Printer(object):
    MAXLINES = 23
    
    def __init__(self, name, data, files = (), dirs = ()):
        self._Printer__name = name
        self._Printer__data = data
        self._Printer__files = files
        self._Printer__dirs = dirs
        self._Printer__lines = None

    
    def _Printer__setup(self):
        if self._Printer__lines:
            return None
        
        data = None
        for dir in self._Printer__dirs:
            for filename in self._Printer__files:
                filename = os.path.join(dir, filename)
                
                try:
                    fp = file(filename, 'rU')
                    data = fp.read()
                    fp.close()
                continue
                except IOError:
                    continue
                

            
            if data:
                break
                continue
        
        if not data:
            data = self._Printer__data
        
        self._Printer__lines = data.split('\n')
        self._Printer__linecnt = len(self._Printer__lines)

    
    def __repr__(self):
        self._Printer__setup()
        if len(self._Printer__lines) <= self.MAXLINES:
            return '\n'.join(self._Printer__lines)
        else:
            return 'Type %s() to see the full %s text' % (self._Printer__name,) * 2

    
    def __call__(self):
        self._Printer__setup()
        prompt = 'Hit Return for more, or q (and Return) to quit: '
        lineno = 0
        while None:
            
            try:
                for i in range(lineno, lineno + self.MAXLINES):
                    print self._Printer__lines[i]
            except IndexError:
                break
                continue

            lineno += self.MAXLINES
            key = None
            while key is None:
                key = raw_input(prompt)
                if key not in ('', 'q'):
                    key = None
                    continue
            if key == 'q':
                break
                continue



def setcopyright():
    __builtin__.copyright = _Printer('copyright', sys.copyright)
    if sys.platform[:4] == 'java':
        __builtin__.credits = _Printer('credits', 'Jython is maintained by the Jython developers (www.jython.org).')
    else:
        __builtin__.credits = _Printer('credits', '    Thanks to CWI, CNRI, BeOpen.com, Zope Corporation and a cast of thousands\n    for supporting Python development.  See www.python.org for more information.')
    here = os.path.dirname(os.__file__)
    __builtin__.license = _Printer('license', 'See http://www.python.org/%.3s/license.html' % sys.version, [
        'LICENSE.txt',
        'LICENSE'], [
        os.path.join(here, os.pardir),
        here,
        os.curdir])


class _Helper(object):
    
    def __repr__(self):
        return 'Type help() for interactive help, or help(object) for help about object.'

    
    def __call__(self, *args, **kwds):
        import pydoc as pydoc
        return pydoc.help(*args, **args)



def sethelper():
    __builtin__.help = _Helper()


def aliasmbcs():
    if sys.platform == 'win32':
        import locale as locale
        import codecs as codecs
        enc = locale.getdefaultlocale()[1]
        if enc.startswith('cp'):
            
            try:
                codecs.lookup(enc)
            except LookupError:
                import encodings as encodings
                encodings._cache[enc] = encodings._unknown
                encodings.aliases.aliases[enc] = 'mbcs'
            

    


def setencoding():
    encoding = 'ascii'
    if encoding != 'ascii':
        sys.setdefaultencoding(encoding)
    


def execsitecustomize():
    
    try:
        import sitecustomize as sitecustomize
    except ImportError:
        pass



def main():
    abs__file__()
    paths_in_sys = removeduppaths()
    if os.name == 'posix' and sys.path and os.path.basename(sys.path[-1]) == 'Modules':
        addbuilddir()
    
    paths_in_sys = addsitepackages(paths_in_sys)
    if sys.platform == 'os2emx':
        setBEGINLIBPATH()
    
    setquit()
    setcopyright()
    sethelper()
    aliasmbcs()
    setencoding()
    execsitecustomize()
    if hasattr(sys, 'setdefaultencoding'):
        del sys.setdefaultencoding
    

main()

def _test():
    print 'sys.path = ['
    for dir in sys.path:
        print '    %r,' % (dir,)
    
    print ']'

if __name__ == '__main__':
    _test()

