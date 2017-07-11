# File: d (Python 2.4)

__all__ = [
    'MiniTask',
    'MiniTaskManager']

class MiniTask:
    done = 0
    cont = 1
    
    def __init__(self, callback):
        self.__call__ = callback



class MiniTaskManager:
    
    def __init__(self):
        self.taskList = []
        self.running = 0

    
    def add(self, task, name):
        task.name = name
        self.taskList.append(task)

    
    def remove(self, task):
        
        try:
            self.taskList.remove(task)
        except ValueError:
            pass


    
    def _MiniTaskManager__executeTask(self, task):
        return task(task)

    
    def step(self):
        i = 0
        while i < len(self.taskList):
            task = self.taskList[i]
            ret = task(task)
            if ret == task.cont:
                pass
            1
            
            try:
                self.taskList.remove(task)
            continue
            except ValueError:
                continue
            

            i += 1

    
    def run(self):
        self.running = 1
        while self.running:
            self.step()

    
    def stop(self):
        self.running = 0


