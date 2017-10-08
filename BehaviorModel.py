from SimObject import *

class BehaviorModel(SimObject):
    def __init__(self, instantiate_time, destruct_time, name):
        self._obj_name = name
        self._instance_t = instantiate_time
        self._destruct_t = destruct_time
        self._next_event_t = 0
        self._state = ""
        self._state_lst = []
        self._time_map = {}
        self._inport_lst = []
        self._outport_lst = []

        self.RequestedTime = float("inf")

    def get_create_time(self):
        return self._instance_t

    def get_destruct_time(self):
        return self._destruct_t

    def get_obj_name(self):
        return self._obj_name

    # state management
    def get_cur_state(self):
        return self._state

    def init_state(self, state):
        self._state = state

    def add_state(self, state, deadline):
        self._time_map[state] = deadline
        self._state_lst.append(state)

    # input port management
    def add_in_port(self, name):
        self._inport_lst.append(name)

    def get_in_port(self):
        return self._inport_lst

    # output port management
    def add_out_port(self, name):
        self._outport_lst.append(name)

    def get_out_port(self):
        return self._outport_lst

    # External Transition
    def ext_trans(self, port, msg):
        return False

    # Internal Transition
    def int_trans(self):
        return False

    # Output Function
    def output(self):
        return None #output function should return Tuple (port name, SimEnvelope)

    # Time Advanced Function
    def time_advance(self):
        if self._state in self._time_map:
            return self._time_map[self._state]
        else:
            return -1

    def set_req_time(self, global_time):
        self.RequestedTime = global_time + self.time_advance()

    def get_req_time(self):
        return self.RequestedTime