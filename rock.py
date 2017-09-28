from peter import *

class Test(SimObject):
    def next_event(self):
        return 0

    def time_advance(self):
        print("Test")
        return 1

    def output(self):
        return None


se = SimEngine()
for i in range(10):
    se.register_agent(Test(i+1, 100, "name"+str(i)))

se.simulate()
