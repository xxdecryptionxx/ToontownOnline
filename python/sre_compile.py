# File: s (Python 2.4)

import _sre
import sys
from sre_constants import *
if _sre.CODESIZE == 2:
    MAXCODE = 65535
else:
    MAXCODE = 0xFFFFFFFFL

def _identityfunction(x):
    return x


def _compile(code, pattern, flags):
    emit = code.append
    _len = len
    LITERAL_CODES = {
        LITERAL: 1,
        NOT_LITERAL: 1 }
    REPEATING_CODES = {
        REPEAT: 1,
        MIN_REPEAT: 1,
        MAX_REPEAT: 1 }
    SUCCESS_CODES = {
        SUCCESS: 1,
        FAILURE: 1 }
    ASSERT_CODES = {
        ASSERT: 1,
        ASSERT_NOT: 1 }
    for (op, av) in pattern:
        if op in LITERAL_CODES:
            if flags & SRE_FLAG_IGNORECASE:
                emit(OPCODES[OP_IGNORE[op]])
                emit(_sre.getlower(av, flags))
            else:
                emit(OPCODES[op])
                emit(av)
        if op is IN:
            if flags & SRE_FLAG_IGNORECASE:
                emit(OPCODES[OP_IGNORE[op]])
                
                def fixup(literal, flags = flags):
                    return _sre.getlower(literal, flags)

            else:
                emit(OPCODES[op])
                fixup = _identityfunction
            skip = _len(code)
            emit(0)
            _compile_charset(av, flags, code, fixup)
            code[skip] = _len(code) - skip
            continue
        if op is ANY:
            if flags & SRE_FLAG_DOTALL:
                emit(OPCODES[ANY_ALL])
            else:
                emit(OPCODES[ANY])
        if op in REPEATING_CODES:
            if flags & SRE_FLAG_TEMPLATE:
                raise error, 'internal: unsupported template operator'
                emit(OPCODES[REPEAT])
                skip = _len(code)
                emit(0)
                emit(av[0])
                emit(av[1])
                _compile(code, av[2], flags)
                emit(OPCODES[SUCCESS])
                code[skip] = _len(code) - skip
            elif _simple(av) and op is not REPEAT:
                if op is MAX_REPEAT:
                    emit(OPCODES[REPEAT_ONE])
                else:
                    emit(OPCODES[MIN_REPEAT_ONE])
                skip = _len(code)
                emit(0)
                emit(av[0])
                emit(av[1])
                _compile(code, av[2], flags)
                emit(OPCODES[SUCCESS])
                code[skip] = _len(code) - skip
            else:
                emit(OPCODES[REPEAT])
                skip = _len(code)
                emit(0)
                emit(av[0])
                emit(av[1])
                _compile(code, av[2], flags)
                code[skip] = _len(code) - skip
                if op is MAX_REPEAT:
                    emit(OPCODES[MAX_UNTIL])
                else:
                    emit(OPCODES[MIN_UNTIL])
        op is MAX_REPEAT
        if op is SUBPATTERN:
            if av[0]:
                emit(OPCODES[MARK])
                emit((av[0] - 1) * 2)
            
            _compile(code, av[1], flags)
            if av[0]:
                emit(OPCODES[MARK])
                emit((av[0] - 1) * 2 + 1)
            
        av[0]
        if op in SUCCESS_CODES:
            emit(OPCODES[op])
            continue
        if op in ASSERT_CODES:
            emit(OPCODES[op])
            skip = _len(code)
            emit(0)
            if av[0] >= 0:
                emit(0)
            else:
                (lo, hi) = av[1].getwidth()
                if lo != hi:
                    raise error, 'look-behind requires fixed-width pattern'
                
                emit(lo)
            _compile(code, av[1], flags)
            emit(OPCODES[SUCCESS])
            code[skip] = _len(code) - skip
            continue
        if op is CALL:
            emit(OPCODES[op])
            skip = _len(code)
            emit(0)
            _compile(code, av, flags)
            emit(OPCODES[SUCCESS])
            code[skip] = _len(code) - skip
            continue
        if op is AT:
            emit(OPCODES[op])
            if flags & SRE_FLAG_MULTILINE:
                av = AT_MULTILINE.get(av, av)
            
            if flags & SRE_FLAG_LOCALE:
                av = AT_LOCALE.get(av, av)
            elif flags & SRE_FLAG_UNICODE:
                av = AT_UNICODE.get(av, av)
            
            emit(ATCODES[av])
            continue
        if op is BRANCH:
            emit(OPCODES[op])
            tail = []
            tailappend = tail.append
            for av in av[1]:
                skip = _len(code)
                emit(0)
                _compile(code, av, flags)
                emit(OPCODES[JUMP])
                tailappend(_len(code))
                emit(0)
                code[skip] = _len(code) - skip
            
            emit(0)
            for tail in tail:
                code[tail] = _len(code) - tail
            
        if op is CATEGORY:
            emit(OPCODES[op])
            if flags & SRE_FLAG_LOCALE:
                av = CH_LOCALE[av]
            elif flags & SRE_FLAG_UNICODE:
                av = CH_UNICODE[av]
            
            emit(CHCODES[av])
            continue
        if op is GROUPREF:
            if flags & SRE_FLAG_IGNORECASE:
                emit(OPCODES[OP_IGNORE[op]])
            else:
                emit(OPCODES[op])
            emit(av - 1)
            continue
        if op is GROUPREF_EXISTS:
            emit(OPCODES[op])
            emit((av[0] - 1) * 2)
            skipyes = _len(code)
            emit(0)
            _compile(code, av[1], flags)
            if av[2]:
                emit(OPCODES[JUMP])
                skipno = _len(code)
                emit(0)
                code[skipyes] = (_len(code) - skipyes) + 1
                _compile(code, av[2], flags)
                code[skipno] = _len(code) - skipno
            else:
                code[skipyes] = (_len(code) - skipyes) + 1
        av[2]
        raise ValueError, ('unsupported operand type', op)
    


def _compile_charset(charset, flags, code, fixup = None):
    emit = code.append
    if fixup is None:
        fixup = _identityfunction
    
    for (op, av) in _optimize_charset(charset, fixup):
        emit(OPCODES[op])
        if op is NEGATE:
            continue
        if op is LITERAL:
            emit(fixup(av))
            continue
        if op is RANGE:
            emit(fixup(av[0]))
            emit(fixup(av[1]))
            continue
        if op is CHARSET:
            code.extend(av)
            continue
        if op is BIGCHARSET:
            code.extend(av)
            continue
        if op is CATEGORY:
            if flags & SRE_FLAG_LOCALE:
                emit(CHCODES[CH_LOCALE[av]])
            elif flags & SRE_FLAG_UNICODE:
                emit(CHCODES[CH_UNICODE[av]])
            else:
                emit(CHCODES[av])
        raise error, 'internal: unsupported set operator'
    
    emit(OPCODES[FAILURE])


def _optimize_charset(charset, fixup):
    out = []
    outappend = out.append
    charmap = [
        0] * 256
    
    try:
        for (op, av) in charset:
            if op is NEGATE:
                outappend((op, av))
                continue
            if op is LITERAL:
                charmap[fixup(av)] = 1
                continue
            if op is RANGE:
                for i in range(fixup(av[0]), fixup(av[1]) + 1):
                    charmap[i] = 1
                
            if op is CATEGORY:
                return charset
                continue
    except IndexError:
        return _optimize_unicode(charset, fixup)

    i = 0
    p = 0
    n = 0
    runs = []
    runsappend = runs.append
    for c in charmap:
        if c:
            if n == 0:
                p = i
            
            n = n + 1
        elif n:
            runsappend((p, n))
            n = 0
        
        i = i + 1
    
    if n:
        runsappend((p, n))
    
    if len(runs) <= 2:
        for (p, n) in runs:
            if n == 1:
                outappend((LITERAL, p))
                continue
            outappend((RANGE, (p, p + n - 1)))
        
        if len(out) < len(charset):
            return out
        
    else:
        data = _mk_bitmap(charmap)
        outappend((CHARSET, data))
        return out
    return charset


def _mk_bitmap(bits):
    data = []
    dataappend = data.append
    if _sre.CODESIZE == 2:
        start = (1, 0)
    else:
        start = (0x1L, 0x0L)
    (m, v) = start
    for c in bits:
        if c:
            v = v + m
        
        m = m + m
        if m > MAXCODE:
            dataappend(v)
            (m, v) = start
            continue
    
    return data


def _optimize_unicode(charset, fixup):
    
    try:
        import array as array
    except ImportError:
        return charset

    charmap = [
        0] * 65536
    negate = 0
    
    try:
        for (op, av) in charset:
            if op is NEGATE:
                negate = 1
                continue
            if op is LITERAL:
                charmap[fixup(av)] = 1
                continue
            if op is RANGE:
                for i in xrange(fixup(av[0]), fixup(av[1]) + 1):
                    charmap[i] = 1
                
            if op is CATEGORY:
                return charset
                continue
    except IndexError:
        return charset

    if negate:
        if sys.maxunicode != 65535:
            return charset
        
        for i in xrange(65536):
            charmap[i] = not charmap[i]
        
    
    comps = { }
    mapping = [
        0] * 256
    block = 0
    data = []
    for i in xrange(256):
        chunk = tuple(charmap[i * 256:(i + 1) * 256])
        new = comps.setdefault(chunk, block)
        mapping[i] = new
        if new == block:
            block = block + 1
            data = data + _mk_bitmap(chunk)
            continue
    
    header = [
        block]
    if _sre.CODESIZE == 2:
        code = 'H'
    else:
        code = 'I'
    mapping = array.array('b', mapping).tostring()
    mapping = array.array(code, mapping)
    header = header + mapping.tolist()
    data[0:0] = header
    return [
        (BIGCHARSET, data)]


def _simple(av):
    (lo, hi) = av[2].getwidth()
    if lo == 0 and hi == MAXREPEAT:
        raise error, 'nothing to repeat'
    
    if lo == hi:
        pass
    hi == 1
    if 1:
        pass
    return av[2][0][0] != SUBPATTERN


def _compile_info(code, pattern, flags):
    (lo, hi) = pattern.getwidth()
    if lo == 0:
        return None
    
    prefix = []
    prefixappend = prefix.append
    prefix_skip = 0
    charset = []
    charsetappend = charset.append
    if not flags & SRE_FLAG_IGNORECASE:
        for (op, av) in pattern.data:
            if op is LITERAL:
                if len(prefix) == prefix_skip:
                    prefix_skip = prefix_skip + 1
                
                prefixappend(av)
                continue
            if op is SUBPATTERN and len(av[1]) == 1:
                (op, av) = av[1][0]
                if op is LITERAL:
                    prefixappend(av)
                else:
                    break
            op is LITERAL
            break
        
        if not prefix and pattern.data:
            (op, av) = pattern.data[0]
            if op is SUBPATTERN and av[1]:
                (op, av) = av[1][0]
                if op is LITERAL:
                    charsetappend((op, av))
                elif op is BRANCH:
                    c = []
                    cappend = c.append
                    for p in av[1]:
                        if not p:
                            break
                        
                        (op, av) = p[0]
                        if op is LITERAL:
                            cappend((op, av))
                            continue
                        break
                    else:
                        charset = c
                
            elif op is BRANCH:
                c = []
                cappend = c.append
                for p in av[1]:
                    if not p:
                        break
                    
                    (op, av) = p[0]
                    if op is LITERAL:
                        cappend((op, av))
                        continue
                    break
                else:
                    charset = c
            elif op is IN:
                charset = av
            
        
    
    emit = code.append
    emit(OPCODES[INFO])
    skip = len(code)
    emit(0)
    mask = 0
    if prefix:
        mask = SRE_INFO_PREFIX
        if len(prefix) == prefix_skip:
            pass
        prefix_skip == len(pattern.data)
        if 1:
            mask = mask + SRE_INFO_LITERAL
        
    elif charset:
        mask = mask + SRE_INFO_CHARSET
    
    emit(mask)
    if lo < MAXCODE:
        emit(lo)
    else:
        emit(MAXCODE)
        prefix = prefix[:MAXCODE]
    if hi < MAXCODE:
        emit(hi)
    else:
        emit(0)
    if prefix:
        emit(len(prefix))
        emit(prefix_skip)
        code.extend(prefix)
        table = [
            -1] + [
            0] * len(prefix)
        for i in xrange(len(prefix)):
            table[i + 1] = table[i] + 1
            while table[i + 1] > 0 and prefix[i] != prefix[table[i + 1] - 1]:
                table[i + 1] = table[table[i + 1] - 1] + 1
        
        code.extend(table[1:])
    elif charset:
        _compile_charset(charset, flags, code)
    
    code[skip] = len(code) - skip


try:
    pass
except NameError:
    STRING_TYPES = (type(''),)

STRING_TYPES = (type(''), type(unicode('')))

def isstring(obj):
    for tp in STRING_TYPES:
        if isinstance(obj, tp):
            return 1
            continue
    
    return 0


def _code(p, flags):
    flags = p.pattern.flags | flags
    code = []
    _compile_info(code, p, flags)
    _compile(code, p.data, flags)
    code.append(OPCODES[SUCCESS])
    return code


def compile(p, flags = 0):
    if isstring(p):
        import sre_parse as sre_parse
        pattern = p
        p = sre_parse.parse(p, flags)
    else:
        pattern = None
    code = _code(p, flags)
    if p.pattern.groups > 100:
        raise AssertionError('sorry, but this version only supports 100 named groups')
    
    groupindex = p.pattern.groupdict
    indexgroup = [
        None] * p.pattern.groups
    for (k, i) in groupindex.items():
        indexgroup[i] = k
    
    return _sre.compile(pattern, flags, code, p.pattern.groups - 1, groupindex, indexgroup)

