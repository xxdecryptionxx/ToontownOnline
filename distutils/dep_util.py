# File: d (Python 2.4)

__revision__ = '$Id: dep_util.py,v 1.1.1.1 2005/04/12 20:52:45 skyler Exp $'
import os
from distutils.errors import DistutilsFileError

def newer(source, target):
    if not os.path.exists(source):
        raise DistutilsFileError, "file '%s' does not exist" % source
    
    if not os.path.exists(target):
        return 1
    
    ST_MTIME = ST_MTIME
    import stat
    mtime1 = os.stat(source)[ST_MTIME]
    mtime2 = os.stat(target)[ST_MTIME]
    return mtime1 > mtime2


def newer_pairwise(sources, targets):
    if len(sources) != len(targets):
        raise ValueError, "'sources' and 'targets' must be same length"
    
    n_sources = []
    n_targets = []
    for i in range(len(sources)):
        if newer(sources[i], targets[i]):
            n_sources.append(sources[i])
            n_targets.append(targets[i])
            continue
    
    return (n_sources, n_targets)


def newer_group(sources, target, missing = 'error'):
    if not os.path.exists(target):
        return 1
    
    ST_MTIME = ST_MTIME
    import stat
    target_mtime = os.stat(target)[ST_MTIME]
    for source in sources:
        if not os.path.exists(source):
            if missing == 'error':
                pass
            elif missing == 'ignore':
                continue
            elif missing == 'newer':
                return 1
            
        
        source_mtime = os.stat(source)[ST_MTIME]
        if source_mtime > target_mtime:
            return 1
            continue
    else:
        return 0

