# File: c (Python 2.4)

import types
from copy_reg import dispatch_table

class Error(Exception):
    pass

error = Error

try:
    from org.python.core import PyStringMap
except ImportError:
    PyStringMap = None

__all__ = [
    'Error',
    'copy',
    'deepcopy']
import inspect

def _getspecial(cls, name):
    for basecls in inspect.getmro(cls):
        
        try:
            return basecls.__dict__[name]
        continue
        continue

    else:
        return None


def copy(x):
    cls = type(x)
    copier = _copy_dispatch.get(cls)
    if copier:
        return copier(x)
    
    copier = _getspecial(cls, '__copy__')
    if copier:
        return copier(x)
    
    reductor = dispatch_table.get(cls)
    if reductor:
        rv = reductor(x)
    else:
        reductor = getattr(x, '__reduce_ex__', None)
        if reductor:
            rv = reductor(2)
        else:
            reductor = getattr(x, '__reduce__', None)
            if reductor:
                rv = reductor()
            else:
                copier = getattr(x, '__copy__', None)
                if copier:
                    return copier()
                
                raise Error('un(shallow)copyable object of type %s' % cls)
    return _reconstruct(x, rv, 0)

_copy_dispatch = { }
d = { }

def _copy_immutable(x):
    return x

for t in (types.NoneType, int, long, float, bool, str, tuple, frozenset, type, xrange, types.ClassType, types.BuiltinFunctionType):
    d[t] = _copy_immutable

for name in ('ComplexType', 'UnicodeType', 'CodeType'):
    t = getattr(types, name, None)
    if t is not None:
        d[t] = _copy_immutable
        continue


def _copy_with_constructor(x):
    return type(x)(x)

for t in (list, dict, set):
    d[t] = _copy_with_constructor


def _copy_with_copy_method(x):
    return x.copy()

if PyStringMap is not None:
    d[PyStringMap] = _copy_with_copy_method


def _copy_inst(x):
    if hasattr(x, '__copy__'):
        return x.__copy__()
    
    if hasattr(x, '__getinitargs__'):
        args = x.__getinitargs__()
        y = x.__class__(*args)
    else:
        y = _EmptyClass()
        y.__class__ = x.__class__
    if hasattr(x, '__getstate__'):
        state = x.__getstate__()
    else:
        state = x.__dict__
    if hasattr(y, '__setstate__'):
        y.__setstate__(state)
    else:
        y.__dict__.update(state)
    return y

d[types.InstanceType] = _copy_inst
del d

def deepcopy(x, memo = None, _nil = []):
    if memo is None:
        memo = { }
    
    d = id(x)
    y = memo.get(d, _nil)
    if y is not _nil:
        return y
    
    cls = type(x)
    copier = _deepcopy_dispatch.get(cls)
    if copier:
        y = copier(x, memo)
    else:
        
        try:
            issc = issubclass(cls, type)
        except TypeError:
            issc = 0

        if issc:
            y = _deepcopy_atomic(x, memo)
        else:
            copier = _getspecial(cls, '__deepcopy__')
            if copier:
                y = copier(x, memo)
            else:
                reductor = dispatch_table.get(cls)
                if reductor:
                    rv = reductor(x)
                else:
                    reductor = getattr(x, '__reduce_ex__', None)
                    if reductor:
                        rv = reductor(2)
                    else:
                        reductor = getattr(x, '__reduce__', None)
                        if reductor:
                            rv = reductor()
                        else:
                            copier = getattr(x, '__deepcopy__', None)
                            if copier:
                                return copier(memo)
                            
                            raise Error('un(deep)copyable object of type %s' % cls)
                y = _reconstruct(x, rv, 1, memo)
    memo[d] = y
    _keep_alive(x, memo)
    return y

_deepcopy_dispatch = { }
d = { }

def _deepcopy_atomic(x, memo):
    return x

d[types.NoneType] = _deepcopy_atomic
d[types.IntType] = _deepcopy_atomic
d[types.LongType] = _deepcopy_atomic
d[types.FloatType] = _deepcopy_atomic
d[types.BooleanType] = _deepcopy_atomic

try:
    d[types.ComplexType] = _deepcopy_atomic
except AttributeError:
    pass

d[types.StringType] = _deepcopy_atomic

try:
    d[types.UnicodeType] = _deepcopy_atomic
except AttributeError:
    pass


try:
    d[types.CodeType] = _deepcopy_atomic
except AttributeError:
    pass

d[types.TypeType] = _deepcopy_atomic
d[types.XRangeType] = _deepcopy_atomic
d[types.ClassType] = _deepcopy_atomic
d[types.BuiltinFunctionType] = _deepcopy_atomic

def _deepcopy_list(x, memo):
    y = []
    memo[id(x)] = y
    for a in x:
        y.append(deepcopy(a, memo))
    
    return y

d[types.ListType] = _deepcopy_list

def _deepcopy_tuple(x, memo):
    y = []
    for a in x:
        y.append(deepcopy(a, memo))
    
    d = id(x)
    
    try:
        return memo[d]
    except KeyError:
        pass

    for i in range(len(x)):
        if x[i] is not y[i]:
            y = tuple(y)
            break
            continue
    else:
        y = x
    memo[d] = y
    return y

d[types.TupleType] = _deepcopy_tuple

def _deepcopy_dict(x, memo):
    y = { }
    memo[id(x)] = y
    for (key, value) in x.iteritems():
        y[deepcopy(key, memo)] = deepcopy(value, memo)
    
    return y

d[types.DictionaryType] = _deepcopy_dict
if PyStringMap is not None:
    d[PyStringMap] = _deepcopy_dict


def _keep_alive(x, memo):
    
    try:
        memo[id(memo)].append(x)
    except KeyError:
        memo[id(memo)] = [
            x]



def _deepcopy_inst(x, memo):
    if hasattr(x, '__deepcopy__'):
        return x.__deepcopy__(memo)
    
    if hasattr(x, '__getinitargs__'):
        args = x.__getinitargs__()
        args = deepcopy(args, memo)
        y = x.__class__(*args)
    else:
        y = _EmptyClass()
        y.__class__ = x.__class__
    memo[id(x)] = y
    if hasattr(x, '__getstate__'):
        state = x.__getstate__()
    else:
        state = x.__dict__
    state = deepcopy(state, memo)
    if hasattr(y, '__setstate__'):
        y.__setstate__(state)
    else:
        y.__dict__.update(state)
    return y

d[types.InstanceType] = _deepcopy_inst

def _reconstruct(x, info, deep, memo = None):
    if isinstance(info, str):
        return x
    
    if memo is None:
        memo = { }
    
    n = len(info)
    (callable, args) = info[:2]
    if n > 2:
        state = info[2]
    else:
        state = { }
    if n > 3:
        listiter = info[3]
    else:
        listiter = None
    if n > 4:
        dictiter = info[4]
    else:
        dictiter = None
    if deep:
        args = deepcopy(args, memo)
    
    y = callable(*args)
    memo[id(x)] = y
    if listiter is not None:
        for item in listiter:
            if deep:
                item = deepcopy(item, memo)
            
            y.append(item)
        
    
    if dictiter is not None:
        for (key, value) in dictiter:
            if deep:
                key = deepcopy(key, memo)
                value = deepcopy(value, memo)
            
            y[key] = value
        
    
    if state:
        if deep:
            state = deepcopy(state, memo)
        
        if hasattr(y, '__setstate__'):
            y.__setstate__(state)
        elif isinstance(state, tuple) and len(state) == 2:
            (state, slotstate) = state
        else:
            slotstate = None
        if state is not None:
            y.__dict__.update(state)
        
        if slotstate is not None:
            for (key, value) in slotstate.iteritems():
                setattr(y, key, value)
            
        
    
    return y

del d
del types

class _EmptyClass:
    pass


def _test():
    l = [
        None,
        1,
        0x2L,
        3.1400000000000001,
        'xyzzy',
        (1, 0x2L),
        [
            3.1400000000000001,
            'abc'],
        {
            'abc': 'ABC' },
        (),
        [],
        { }]
    l1 = copy(l)
    print l1 == l
    l1 = map(copy, l)
    print l1 == l
    l1 = deepcopy(l)
    print l1 == l
    
    class C:
        
        def __init__(self, arg = None):
            self.a = 1
            self.arg = arg
            if __name__ == '__main__':
                import sys as sys
                file = sys.argv[0]
            else:
                file = __file__
            self.fp = open(file)
            self.fp.close()

        
        def __getstate__(self):
            return {
                'a': self.a,
                'arg': self.arg }

        
        def __setstate__(self, state):
            for (key, value) in state.iteritems():
                setattr(self, key, value)
            

        
        def __deepcopy__(self, memo = None):
            new = self.__class__(deepcopy(self.arg, memo))
            new.a = self.a
            return new


    c = C('argument sketch')
    l.append(c)
    l2 = copy(l)
    print l == l2
    print l
    print l2
    l2 = deepcopy(l)
    print l == l2
    print l
    print l2
    l.append({
        l[1]: l,
        'xyz': l[2] })
    l3 = copy(l)
    import repr as repr
    print map(repr.repr, l)
    print map(repr.repr, l1)
    print map(repr.repr, l2)
    print map(repr.repr, l3)
    l3 = deepcopy(l)
    import repr as repr
    print map(repr.repr, l)
    print map(repr.repr, l1)
    print map(repr.repr, l2)
    print map(repr.repr, l3)

if __name__ == '__main__':
    _test()
