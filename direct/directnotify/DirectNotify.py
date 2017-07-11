# File: d (Python 2.4)

import Notifier
import Logger

class DirectNotify:
    
    def __init__(self):
        self._DirectNotify__categories = { }
        self.logger = Logger.Logger()
        self.streamWriter = None

    
    def __str__(self):
        return 'DirectNotify categories: %s' % self._DirectNotify__categories

    
    def getCategories(self):
        return self._DirectNotify__categories.keys()

    
    def getCategory(self, categoryName):
        return self._DirectNotify__categories.get(categoryName, None)

    
    def newCategory(self, categoryName, logger = None):
        if categoryName not in self._DirectNotify__categories:
            self._DirectNotify__categories[categoryName] = Notifier.Notifier(categoryName, logger)
            self.setDconfigLevel(categoryName)
        
        return self.getCategory(categoryName)

    
    def setDconfigLevel(self, categoryName):
        
        try:
            pass
        except:
            return 0

        dconfigParam = 'notify-level-' + categoryName
        level = config.GetString(dconfigParam, '')
        if not level:
            level = config.GetString('default-directnotify-level', 'info')
        
        if not level:
            level = 'error'
        
        category = self.getCategory(categoryName)
        if level == 'error':
            category.setWarning(0)
            category.setInfo(0)
            category.setDebug(0)
        elif level == 'warning':
            category.setWarning(1)
            category.setInfo(0)
            category.setDebug(0)
        elif level == 'info':
            category.setWarning(1)
            category.setInfo(1)
            category.setDebug(0)
        elif level == 'debug':
            category.setWarning(1)
            category.setInfo(1)
            category.setDebug(1)
        else:
            print 'DirectNotify: unknown notify level: ' + str(level) + ' for category: ' + str(categoryName)

    
    def setDconfigLevels(self):
        for categoryName in self.getCategories():
            self.setDconfigLevel(categoryName)
        

    
    def setVerbose(self):
        for categoryName in self.getCategories():
            category = self.getCategory(categoryName)
            category.setWarning(1)
            category.setInfo(1)
            category.setDebug(1)
        

    
    def popupControls(self, tl = None):
        NotifyPanel = NotifyPanel
        import direct.tkpanels
        NotifyPanel.NotifyPanel(self, tl)

    
    def giveNotify(self, cls):
        cls.notify = self.newCategory(cls.__name__)


