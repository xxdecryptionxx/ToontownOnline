# File: d (Python 2.4)

__revision__ = '$Id: spawn.py,v 1.1.1.1 2005/04/12 20:52:45 skyler Exp $'
import sys
import os
import string
from distutils.errors import *
from distutils import log

def spawn(cmd, search_path = 1, verbose = 0, dry_run = 0):
    if os.name == 'posix':
        _spawn_posix(cmd, search_path, dry_run = dry_run)
    elif os.name == 'nt':
        _spawn_nt(cmd, search_path, dry_run = dry_run)
    elif os.name == 'os2':
        _spawn_os2(cmd, search_path, dry_run = dry_run)
    else:
        raise DistutilsPlatformError, "don't know how to spawn programs on platform '%s'" % os.name


def _nt_quote_args(args):
    for i in range(len(args)):
        if string.find(args[i], ' ') != -1:
            args[i] = '"%s"' % args[i]
            continue
    
    return args


def _spawn_nt(cmd, search_path = 1, verbose = 0, dry_run = 0):
    executable = cmd[0]
    cmd = _nt_quote_args(cmd)
    if search_path:
        if not find_executable(executable):
            pass
        executable = executable
    
    log.info(string.join([
        executable] + cmd[1:], ' '))
    if not dry_run:
        
        try:
            rc = os.spawnv(os.P_WAIT, executable, cmd)
        except OSError:
            exc = None
            raise DistutilsExecError, "command '%s' failed: %s" % (cmd[0], exc[-1])

        if rc != 0:
            raise DistutilsExecError, "command '%s' failed with exit status %d" % (cmd[0], rc)
        
    


def _spawn_os2(cmd, search_path = 1, verbose = 0, dry_run = 0):
    executable = cmd[0]
    if search_path:
        if not find_executable(executable):
            pass
        executable = executable
    
    log.info(string.join([
        executable] + cmd[1:], ' '))
    if not dry_run:
        
        try:
            rc = os.spawnv(os.P_WAIT, executable, cmd)
        except OSError:
            exc = None
            raise DistutilsExecError, "command '%s' failed: %s" % (cmd[0], exc[-1])

        if rc != 0:
            print "command '%s' failed with exit status %d" % (cmd[0], rc)
            raise DistutilsExecError, "command '%s' failed with exit status %d" % (cmd[0], rc)
        
    


def _spawn_posix(cmd, search_path = 1, verbose = 0, dry_run = 0):
    log.info(string.join(cmd, ' '))
    if dry_run:
        return None
    
    if not search_path or os.execvp:
        pass
    exec_fn = os.execv
    pid = os.fork()
    if pid == 0:
        
        try:
            exec_fn(cmd[0], cmd)
        except OSError:
            e = None
            sys.stderr.write('unable to execute %s: %s\n' % (cmd[0], e.strerror))
            os._exit(1)

        sys.stderr.write('unable to execute %s for unknown reasons' % cmd[0])
        os._exit(1)
    else:
        while None:
            
            try:
                (pid, status) = os.waitpid(pid, 0)
            except OSError:
                exc = None
                import errno as errno
                if exc.errno == errno.EINTR:
                    continue
                
                raise DistutilsExecError, "command '%s' failed: %s" % (cmd[0], exc[-1])

            if os.WIFSIGNALED(status):
                raise DistutilsExecError, "command '%s' terminated by signal %d" % (cmd[0], os.WTERMSIG(status))
                continue
            if os.WIFEXITED(status):
                exit_status = os.WEXITSTATUS(status)
                if exit_status == 0:
                    return None
                else:
                    raise DistutilsExecError, "command '%s' failed with exit status %d" % (cmd[0], exit_status)
            exit_status == 0
            if os.WIFSTOPPED(status):
                continue
                continue
            raise DistutilsExecError, "unknown error executing '%s': termination status %d" % (cmd[0], status)


def find_executable(executable, path = None):
    if path is None:
        path = os.environ['PATH']
    
    paths = string.split(path, os.pathsep)
    (base, ext) = os.path.splitext(executable)
    if (sys.platform == 'win32' or os.name == 'os2') and ext != '.exe':
        executable = executable + '.exe'
    
    if not os.path.isfile(executable):
        for p in paths:
            f = os.path.join(p, executable)
            if os.path.isfile(f):
                return f
                continue
        
        return None
    else:
        return executable

