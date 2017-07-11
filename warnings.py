# File: w (Python 2.4)

import sys
import types
import linecache
__all__ = [
    'warn',
    'showwarning',
    'formatwarning',
    'filterwarnings',
    'resetwarnings']
filters = []
defaultaction = 'default'
onceregistry = { }

def warn(message, category = None, stacklevel = 1):
    if isinstance(message, Warning):
        category = message.__class__
    
    if category is None:
        category = UserWarning
    
    
    try:
        caller = sys._getframe(stacklevel)
    except ValueError:
        globals = sys.__dict__
        lineno = 1

    globals = caller.f_globals
    lineno = caller.f_lineno
    if '__name__' in globals:
        module = globals['__name__']
    else:
        module = '<string>'
    filename = globals.get('__file__')
    if filename:
        fnl = filename.lower()
        if fnl.endswith('.pyc') or fnl.endswith('.pyo'):
            filename = filename[:-1]
        
    elif module == '__main__':
        filename = sys.argv[0]
    
    if not filename:
        filename = module
    
    registry = globals.setdefault('__warningregistry__', { })
    warn_explicit(message, category, filename, lineno, module, registry)


def warn_explicit(message, category, filename, lineno, module = None, registry = None):
    if module is None:
        module = filename
        if module[-3:].lower() == '.py':
            module = module[:-3]
        
    
    if registry is None:
        registry = { }
    
    if isinstance(message, Warning):
        text = str(message)
        category = message.__class__
    else:
        text = message
        message = category(message)
    key = (text, category, lineno)
    if registry.get(key):
        return None
    
    for item in filters:
        (action, msg, cat, mod, ln) = item
        if (msg is None or msg.match(text)) and issubclass(category, cat):
            if mod is None or mod.match(module):
                if ln == 0 or lineno == ln:
                    break
                    continue
    else:
        action = defaultaction
    if action == 'ignore':
        registry[key] = 1
        return None
    
    if action == 'error':
        raise message
    
    if action == 'once':
        registry[key] = 1
        oncekey = (text, category)
        if onceregistry.get(oncekey):
            return None
        
        onceregistry[oncekey] = 1
    elif action == 'always':
        pass
    elif action == 'module':
        registry[key] = 1
        altkey = (text, category, 0)
        if registry.get(altkey):
            return None
        
        registry[altkey] = 1
    elif action == 'default':
        registry[key] = 1
    else:
        raise RuntimeError('Unrecognized action (%r) in warnings.filters:\n %s' % (action, item))
    showwarning(message, category, filename, lineno)


def showwarning(message, category, filename, lineno, file = None):
    if file is None:
        file = sys.stderr
    
    
    try:
        file.write(formatwarning(message, category, filename, lineno))
    except IOError:
        pass



def formatwarning(message, category, filename, lineno):
    s = '%s:%s: %s: %s\n' % (filename, lineno, category.__name__, message)
    line = linecache.getline(filename, lineno).strip()
    if line:
        s = s + '  ' + line + '\n'
    
    return s


def filterwarnings(action, message = '', category = Warning, module = '', lineno = 0, append = 0):
    import re as re
    item = (action, re.compile(message, re.I), category, re.compile(module), lineno)
    if append:
        filters.append(item)
    else:
        filters.insert(0, item)


def simplefilter(action, category = Warning, lineno = 0, append = 0):
    item = (action, None, category, None, lineno)
    if append:
        filters.append(item)
    else:
        filters.insert(0, item)


def resetwarnings():
    filters[:] = []


class _OptionError(Exception):
    pass


def _processoptions(args):
    for arg in args:
        
        try:
            _setoption(arg)
        continue
        except _OptionError:
            msg = None
            print >>sys.stderr, 'Invalid -W option ignored:', msg
            continue
        

    


def _setoption(arg):
    import re
    parts = arg.split(':')
    if len(parts) > 5:
        raise _OptionError('too many fields (max 5): %r' % (arg,))
    
    while len(parts) < 5:
        parts.append('')
    continue
    (action, message, category, module, lineno) = [ s.strip() for s in parts ]
    action = _getaction(action)
    message = re.escape(message)
    category = _getcategory(category)
    module = re.escape(module)
    if module:
        module = module + '$'
    
    if lineno:
        
        try:
            lineno = int(lineno)
            if lineno < 0:
                raise ValueError
        except (ValueError, OverflowError):
            []
            raise _OptionError('invalid lineno %r' % (lineno,))
        

    lineno = 0
    filterwarnings(action, message, category, module, lineno)


def _getaction(action):
    if not action:
        return 'default'
    
    if action == 'all':
        return 'always'
    
    for a in [
        'default',
        'always',
        'ignore',
        'module',
        'once',
        'error']:
        if a.startswith(action):
            return a
            continue
    
    raise _OptionError('invalid action: %r' % (action,))


def _getcategory(category):
    import re
    if not category:
        return Warning
    
    if re.match('^[a-zA-Z0-9_]+$', category):
        
        try:
            cat = eval(category)
        except NameError:
            raise _OptionError('unknown warning category: %r' % (category,))
        

    i = category.rfind('.')
    module = category[:i]
    klass = category[i + 1:]
    
    try:
        m = __import__(module, None, None, [
            klass])
    except ImportError:
        raise _OptionError('invalid module name: %r' % (module,))

    
    try:
        cat = getattr(m, klass)
    except AttributeError:
        raise _OptionError('unknown warning category: %r' % (category,))

    if not isinstance(cat, types.ClassType) or not issubclass(cat, Warning):
        raise _OptionError('invalid warning category: %r' % (category,))
    
    return cat

_processoptions(sys.warnoptions)
simplefilter('ignore', category = OverflowWarning, append = 1)
simplefilter('ignore', category = PendingDeprecationWarning, append = 1)
