from peter import *

class Test(SimObject):
    def next_event(self):
        return 0


se = SimEngine()
for i in range(10):
    se.register_agent(Test(0))

se.schedule()

