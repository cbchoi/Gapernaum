#from peter import *
#import datetime

from BehaviorModel import *
from SimEnvelop import *
from SimEngine import *

se = SimEngine()

class Human(BehaviorModel):
    def __init__(self, instance_time, destruct_time, name):
        BehaviorModel.__init__(self, instance_time, destruct_time, name)
        self.x = 0
        self.y = 0
        self.spd = 10

        self.init_state("IDLE")
        self.add_state("IDLE", 0)
        self.add_state("MOVE", 1)

        self.add_in_port("greeting")
        self.add_out_port("hello")

    def ext_trans(self,port, msg):
        data = msg.retrieve()
        print(data[0])

    def output(self):
        self.x += self.spd
        self.y += self.spd

        temp = "[%f] (%d, %d)" % (se.get_global_time(), self.x, self.y)
        print(temp)
        msg = SimEnvelope(self.get_obj_name(), "hello")
        print(str(datetime.datetime.now()) + " Human Object:")
        msg.insert("I am")
        return msg

    def int_trans(self):
        if self._state == "IDLE":
            self._state = "MOVE"
        else:
            self._state = "MOVE"


class Receiver(BehaviorModel):
    def __init__(self, instance_time, destruct_time, name):
        BehaviorModel.__init__(self, instance_time, destruct_time, name)
        self.x = 0
        self.y = 0
        self.spd = 10

        self.init_state("MOVE")
        self.add_state("MOVE", 1)

        self.add_in_port("greeting")

    def ext_trans(self,port, msg):
        data = msg.retrieve()
        #print(str(datetime.datetime.now()) +  " " + str(data[0]))
        temp = "[%f] %s" % (se.get_global_time(), str(data[0]))
        print(temp)

    def output(self):
        temp = "[%f] %s" % (se.get_global_time(), "Human Receiver Object: Move")
        print(temp)
        return None

    def int_trans(self):
            self._state = "MOVE"


h = Human(0, 100, "Peter")
r = Receiver(0, 100, "Simon")
se.register_agent(h)
se.register_agent(r)
se.coupling_relation(h, "hello", r, "greeting")

se.simulate()
