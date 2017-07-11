# File: t (Python 2.4)

import DistributedSZTreasureAI

class DistributedOZTreasureAI(DistributedSZTreasureAI.DistributedSZTreasureAI):
    
    def __init__(self, air, treasurePlanner, x, y, z):
        DistributedSZTreasureAI.DistributedSZTreasureAI.__init__(self, air, treasurePlanner, x, y, z)


