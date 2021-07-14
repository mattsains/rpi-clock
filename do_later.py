from threading import Thread
from time import sleep

# I apologise for this file

class Fork(Thread):
    def __init__(self, func):
        Thread.__init__(self)
        self.func = func
        self.start()
    
    def run(self):
        self.func()

class DoLater:
    def __init__(self, func, seconds):
        def laterer():
            sleep(seconds)
            func()
        Fork(laterer)

class RepeatLater:
    def __init__(self, func, seconds):
        def repeater():
            while (True):
                sleep(seconds)
                func()
        Fork(repeater)
    