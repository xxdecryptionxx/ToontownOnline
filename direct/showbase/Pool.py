# File: d (Python 2.4)

__all__ = [
    'Pool']
from direct.directnotify import DirectNotifyGlobal

class Pool:
    notify = DirectNotifyGlobal.directNotify.newCategory('Pool')
    
    def __init__(self, free = None):
        if free:
            self._Pool__free = free
        else:
            self._Pool__free = []
        self._Pool__used = []

    
    def add(self, item):
        self._Pool__free.append(item)

    
    def remove(self, item):
        if item in self._Pool__free:
            self._Pool__free.remove(item)
        elif item in self._Pool__used:
            self._Pool__used.remove(item)
        else:
            self.notify.error('item not in pool')

    
    def checkout(self):
        if not self._Pool__free:
            self.notify.error('no items are free')
        
        item = self._Pool__free.pop()
        self._Pool__used.append(item)
        return item

    
    def checkin(self, item):
        if item not in self._Pool__used:
            self.notify.error('item is not checked out')
        
        self._Pool__used.remove(item)
        self._Pool__free.append(item)

    
    def reset(self):
        self._Pool__free.extend(self._Pool__used)
        self._Pool__used = []

    
    def hasFree(self):
        return len(self._Pool__free) != 0

    
    def isFree(self, item):
        return item in self._Pool__free

    
    def isUsed(self, item):
        return item in self._Pool__used

    
    def getNumItems(self):
        return (len(self._Pool__free), len(self._Pool__used))

    
    def cleanup(self, cleanupFunc = None):
        if cleanupFunc:
            allItems = self._Pool__free + self._Pool__used
            for item in allItems:
                cleanupFunc(item)
            
        
        del self._Pool__free
        del self._Pool__used

    
    def __repr__(self):
        return 'free = %s\nused = %s' % (self._Pool__free, self._Pool__used)


