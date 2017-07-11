# File: l (Python 2.4)

global cache
import sys
import os
__all__ = [
    'getline',
    'clearcache',
    'checkcache']

def getline(filename, lineno):
    lines = getlines(filename)
    if 1 <= lineno:
        pass
    lineno <= len(lines)
    if 1:
        return lines[lineno - 1]
    else:
        return ''

cache = { }

def clearcache():
    global cache
    cache = { }


def getlines(filename):
    if filename in cache:
        return cache[filename][2]
    else:
        return updatecache(filename)


def checkcache(filename = None):
    if filename is None:
        filenames = cache.keys()
    elif filename in cache:
        filenames = [
            filename]
    else:
        return None
    for filename in filenames:
        (size, mtime, lines, fullname) = cache[filename]
        
        try:
            stat = os.stat(fullname)
        except os.error:
            del cache[filename]
            continue

        if size != stat.st_size or mtime != stat.st_mtime:
            del cache[filename]
            continue
    


def updatecache(filename):
    if filename in cache:
        del cache[filename]
    
    if not filename or filename[0] + filename[-1] == '<>':
        return []
    
    fullname = filename
    
    try:
        stat = os.stat(fullname)
    except os.error:
        msg = None
        basename = os.path.split(filename)[1]
        for dirname in sys.path:
            
            try:
                fullname = os.path.join(dirname, basename)
            except (TypeError, AttributeError):
                continue

            
            try:
                stat = os.stat(fullname)
            continue
            except os.error:
                continue
            

        else:
            return []

    
    try:
        fp = open(fullname, 'rU')
        lines = fp.readlines()
        fp.close()
    except IOError:
        msg = None
        return []

    size = stat.st_size
    mtime = stat.st_mtime
    cache[filename] = (size, mtime, lines, fullname)
    return lines

