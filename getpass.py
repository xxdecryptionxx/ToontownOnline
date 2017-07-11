# File: g (Python 2.4)

import sys
__all__ = [
    'getpass',
    'getuser']

def unix_getpass(prompt = 'Password: '):
    
    try:
        fd = sys.stdin.fileno()
    except:
        return default_getpass(prompt)

    old = termios.tcgetattr(fd)
    new = old[:]
    new[3] = new[3] & ~(termios.ECHO)
    
    try:
        termios.tcsetattr(fd, termios.TCSADRAIN, new)
        passwd = _raw_input(prompt)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old)

    sys.stdout.write('\n')
    return passwd


def win_getpass(prompt = 'Password: '):
    if sys.stdin is not sys.__stdin__:
        return default_getpass(prompt)
    
    import msvcrt as msvcrt
    for c in prompt:
        msvcrt.putch(c)
    
    pw = ''
    while None:
        c = msvcrt.getch()
        if c == '\r' or c == '\n':
            break
        
        if c == '\x3':
            raise KeyboardInterrupt
        
        if c == '\x8':
            pw = pw[:-1]
            continue
        pw = pw + c
    msvcrt.putch('\r')
    msvcrt.putch('\n')
    return pw


def default_getpass(prompt = 'Password: '):
    print 'Warning: Problem with getpass. Passwords may be echoed.'
    return _raw_input(prompt)


def _raw_input(prompt = ''):
    prompt = str(prompt)
    if prompt:
        sys.stdout.write(prompt)
    
    line = sys.stdin.readline()
    if not line:
        raise EOFError
    
    if line[-1] == '\n':
        line = line[:-1]
    
    return line


def getuser():
    import os as os
    for name in ('LOGNAME', 'USER', 'LNAME', 'USERNAME'):
        user = os.environ.get(name)
        if user:
            return user
            continue
    
    import pwd as pwd
    return pwd.getpwuid(os.getuid())[0]


try:
    import termios
    (termios.tcgetattr, termios.tcsetattr)
except (ImportError, AttributeError):
    
    try:
        import msvcrt
    except ImportError:
        
        try:
            from EasyDialogs import AskPassword
        except ImportError:
            getpass = default_getpass

        getpass = AskPassword

    getpass = win_getpass

getpass = unix_getpass
