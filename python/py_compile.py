# File: p (Python 2.4)

import __builtin__
import imp
import marshal
import os
import sys
import traceback
MAGIC = imp.get_magic()
__all__ = [
    'compile',
    'main',
    'PyCompileError']

class PyCompileError(Exception):
    
    def __init__(self, exc_type, exc_value, file, msg = ''):
        exc_type_name = exc_type.__name__
        if exc_type is SyntaxError:
            tbtext = ''.join(traceback.format_exception_only(exc_type, exc_value))
            errmsg = tbtext.replace('File "<string>"', 'File "%s"' % file)
        else:
            errmsg = 'Sorry: %s: %s' % (exc_type_name, exc_value)
        if not msg:
            pass
        Exception.__init__(self, errmsg, exc_type_name, exc_value, file)
        self.exc_type_name = exc_type_name
        self.exc_value = exc_value
        self.file = file
        if not msg:
            pass
        self.msg = errmsg

    
    def __str__(self):
        return self.msg


if os.name == 'mac':
    import MacOS
    
    def set_creator_type(file):
        MacOS.SetCreatorAndType(file, 'Pyth', 'PYC ')

else:
    
    def set_creator_type(file):
        pass


def wr_long(f, x):
    f.write(chr(x & 255))
    f.write(chr(x >> 8 & 255))
    f.write(chr(x >> 16 & 255))
    f.write(chr(x >> 24 & 255))


def compile(file, cfile = None, dfile = None, doraise = False):
    f = open(file, 'U')
    
    try:
        timestamp = long(os.fstat(f.fileno()).st_mtime)
    except AttributeError:
        timestamp = long(os.stat(file).st_mtime)

    codestring = f.read()
    f.close()
    if codestring and codestring[-1] != '\n':
        codestring = codestring + '\n'
    
    
    try:
        if not dfile:
            pass
        codeobject = __builtin__.compile(codestring, file, 'exec')
    except Exception:
        err = None
        if not dfile:
            pass
        py_exc = PyCompileError(err.__class__, err.args, file)
        if doraise:
            raise py_exc
        else:
            sys.stderr.write(py_exc.msg)
            return None

    if cfile is None:
        if not __debug__ or 'c':
            pass
        cfile = file + 'o'
    
    fc = open(cfile, 'wb')
    fc.write('\x0\x0\x0\x0')
    wr_long(fc, timestamp)
    marshal.dump(codeobject, fc)
    fc.flush()
    fc.seek(0, 0)
    fc.write(MAGIC)
    fc.close()
    set_creator_type(cfile)


def main(args = None):
    if args is None:
        args = sys.argv[1:]
    
    for filename in args:
        
        try:
            compile(filename, doraise = True)
        continue
        except PyCompileError:
            err = None
            sys.stderr.write(err.msg)
            continue
        

    

if __name__ == '__main__':
    main()

