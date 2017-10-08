from peter import *
import datetime

class Human(SimObject):
    def __init__(self, instance_time, destruct_time, name):
        SimObject.__init__(self, instance_time, destruct_time, name)
        self.x = 0
        self.y = 0
        self.spd = 10

        self.state = "IDLE"
        self.add_state("IDLE", 0)
        self.add_state("MOVE", 1)

        self.add_in_port("greeting")
        self.add_out_port("hello")

    def ext_trans(self,port, msg):
        data = msg.retrive()
        print(data[0])

    def output(self):
        self.x += self.spd
        self.y += self.spd

        print(str(self.x) +"," +str(self.y))
        msg = SimEnvelope(self.get_obj_name(), "hello")
        print(str(datetime.datetime.now()) + " Human Object:")
        msg.insert("I am")

        return msg
    def int_trans(self):
        if self.state == "IDLE":
            self.state = "MOVE"
        else:
            self.state = "MOVE"


class Receiver(SimObject):
    def __init__(self, instance_time, destruct_time, name):
        SimObject.__init__(self, instance_time, destruct_time, name)
        self.x = 0
        self.y = 0
        self.spd = 10

        self.state = "MOVE"
        self.add_state("MOVE", 1)

        self.add_in_port("greeting")

    def ext_trans(self,port, msg):
        data = msg.retrive()
        print(str(datetime.datetime.now()) +  " " + str(data[0]))

    def output(self):
        print(str(datetime.datetime.now()) + " " + "Human Receiver Object:" + "Hello")
        return None

    def int_trans(self):
            self.state = "MOVE"

se = SimEngine()
h = Human(0, 100, "Peter")
r = Receiver(0, 100, "Simon")
se.register_agent(h)
se.register_agent(r)
se.coupling_relation(h, "hello", r, "greeting")

se.simulate()
