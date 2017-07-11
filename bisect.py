# File: b (Python 2.4)


def insort_right(a, x, lo = 0, hi = None):
    if hi is None:
        hi = len(a)
    
    while lo < hi:
        mid = (lo + hi) // 2
        if x < a[mid]:
            hi = mid
            continue
        lo = mid + 1
    a.insert(lo, x)

insort = insort_right

def bisect_right(a, x, lo = 0, hi = None):
    if hi is None:
        hi = len(a)
    
    while lo < hi:
        mid = (lo + hi) // 2
        if x < a[mid]:
            hi = mid
            continue
        lo = mid + 1
    return lo

bisect = bisect_right

def insort_left(a, x, lo = 0, hi = None):
    if hi is None:
        hi = len(a)
    
    while lo < hi:
        mid = (lo + hi) // 2
        if a[mid] < x:
            lo = mid + 1
            continue
        hi = mid
    a.insert(lo, x)


def bisect_left(a, x, lo = 0, hi = None):
    if hi is None:
        hi = len(a)
    
    while lo < hi:
        mid = (lo + hi) // 2
        if a[mid] < x:
            lo = mid + 1
            continue
        hi = mid
    return lo


try:
    from _bisect import bisect_right, bisect_left, insort_left, insort_right, insort, bisect
except ImportError:
    pass

