from threading import Thread
from time import sleep

# I apologise for this file

class DoLater(Thread):
    def __init__(self, func, seconds):
        Thread.__init__(self)
        self.func = func
        self.seconds = seconds
        self.start()
    
    def run(self):
        sleep(self.seconds)
        self.func()

class RepeatLater(Thread):
    def __init__(self, func, seconds):
        Thread.__init__(self)
        self.func = func
        self.seconds = seconds
        self.start()
    
    def run(self):
        while (True):
            sleep(self.seconds)
            self.func()