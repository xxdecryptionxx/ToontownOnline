# File: m (Python 2.4)

import os
from stat import *
__all__ = [
    'normcase',
    'isabs',
    'join',
    'splitdrive',
    'split',
    'splitext',
    'basename',
    'dirname',
    'commonprefix',
    'getsize',
    'getmtime',
    'getatime',
    'getctime',
    'islink',
    'exists',
    'isdir',
    'isfile',
    'walk',
    'expanduser',
    'expandvars',
    'normpath',
    'abspath',
    'curdir',
    'pardir',
    'sep',
    'pathsep',
    'defpath',
    'altsep',
    'extsep',
    'devnull',
    'realpath',
    'supports_unicode_filenames']
curdir = ':'
pardir = '::'
extsep = '.'
sep = ':'
pathsep = '\n'
defpath = ':'
altsep = None
devnull = 'Dev:Null'

def normcase(path):
    return path.lower()


def isabs(s):
    if ':' in s:
        pass
    return s[0] != ':'


def join(s, *p):
    path = s
    for t in p:
        if not s or isabs(t):
            path = t
            continue
        
        if t[:1] == ':':
            t = t[1:]
        
        if ':' not in path:
            path = ':' + path
        
        if path[-1:] != ':':
            path = path + ':'
        
        path = path + t
    
    return path


def split(s):
    if ':' not in s:
        return ('', s)
    
    colon = 0
    for i in range(len(s)):
        if s[i] == ':':
            colon = i + 1
            continue
    
    path = s[:colon - 1]
    file = s[colon:]
    if path and ':' not in path:
        path = path + ':'
    
    return (path, file)


def splitext(p):
    i = p.rfind('.')
    if i <= p.rfind(':'):
        return (p, '')
    else:
        return (p[:i], p[i:])


def splitdrive(p):
    return ('', p)


def dirname(s):
    return split(s)[0]


def basename(s):
    return split(s)[1]


def ismount(s):
    if not isabs(s):
        return False
    
    components = split(s)
    if len(components) == 2:
        pass
    return components[1] == ''


def isdir(s):
    
    try:
        st = os.stat(s)
    except os.error:
        return 0

    return S_ISDIR(st.st_mode)


def getsize(filename):
    return os.stat(filename).st_size


def getmtime(filename):
    return os.stat(filename).st_mtime


def getatime(filename):
    return os.stat(filename).st_atime


def islink(s):
    
    try:
        import Carbon.File as Carbon
        return Carbon.File.ResolveAliasFile(s, 0)[2]
    except:
        return False



def isfile(s):
    
    try:
        st = os.stat(s)
    except os.error:
        return False

    return S_ISREG(st.st_mode)


def getctime(filename):
    return os.stat(filename).st_ctime


def exists(s):
    
    try:
        st = os.stat(s)
    except os.error:
        return False

    return True


def lexists(path):
    
    try:
        st = os.lstat(path)
    except os.error:
        return False

    return True


def commonprefix(m):
    if not m:
        return ''
    
    prefix = m[0]
    for item in m:
        for i in range(len(prefix)):
            if prefix[:i + 1] != item[:i + 1]:
                prefix = prefix[:i]
                if i == 0:
                    return ''
                
                break
                continue
        
    
    return prefix


def expandvars(path):
    return path


def expanduser(path):
    return path


class norm_error(Exception):
    pass


def normpath(s):
    if ':' not in s:
        return ':' + s
    
    comps = s.split(':')
    i = 1
    while i < len(comps) - 1:
        if comps[i] == '' and comps[i - 1] != '':
            if i > 1:
                del comps[i - 1:i + 1]
                i = i - 1
            else:
                raise norm_error, 'Cannot use :: immediately after volume name'
        i > 1
        i = i + 1
    s = ':'.join(comps)
    if s[-1] == ':' and len(comps) > 2 and s != ':' * len(s):
        s = s[:-1]
    
    return s


def walk(top, func, arg):
    
    try:
        names = os.listdir(top)
    except os.error:
        return None

    func(arg, top, names)
    for name in names:
        name = join(top, name)
        if isdir(name) and not islink(name):
            walk(name, func, arg)
            continue
    


def abspath(path):
    if not isabs(path):
        path = join(os.getcwd(), path)
    
    return normpath(path)


def realpath(path):
    path = abspath(path)
    
    try:
        import Carbon.File as Carbon
    except ImportError:
        return path

    if not path:
        return path
    
    components = path.split(':')
    path = components[0] + ':'
    for c in components[1:]:
        path = join(path, c)
        path = Carbon.File.FSResolveAliasFile(path, 1)[0].as_pathname()
    
    return path

supports_unicode_filenames = False
