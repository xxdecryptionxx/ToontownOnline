# File: t (Python 2.4)

import Street

class DLStreet(Street.Street):
    
    def __init__(self, loader, parentFSM, doneEvent):
        Street.Street.__init__(self, loader, parentFSM, doneEvent)

    
    def load(self):
        Street.Street.load(self)

    
    def unload(self):
        Street.Street.unload(self)

