__author__ = 'root'
from threading import Thread


class myClassA(Thread):
    a = 0
    def __init__(self):
        Thread.__init__(self)
        self.daemon = True
        self.start()
    def run(self):
        while True:
            if self.a == 0:
                print 'A'
                self.a = 1
            else:
                print 'B'
                self.a = 0

            if self.a == 2:
                print 'C'
                self.a = 3
            else:
                print 'D'
                self.a = 2

class myClassB(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.daemon = True
        self.start()
    def run(self):
        while True:
            print 'B'


c = myClassA()
c.a = 0
cc = myClassA()
cc.a = 2
#myClassB()
while True:
    pass