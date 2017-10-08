from operator import itemgetter

class SimEngine(object):
    EXTERNAL_SRC = "ExternSRC"
    EXTERNAL_DST = "ExternDST"

    def __init__(self, time_step = 1, hierarchical = False):
        self.hierachical = hierarchical
        self.global_time = 0
        self.time_step = time_step

        #dictionary for wating simulation objects
        self.waiting_obj_map = {}
        # dictionary for active simulation objects
        self.active_obj_map = {}
        #dictionary for object to ports
        self.port_map = {}

        self.min_schedule_item = list()

    # retrive global time
    def get_global_time(self):
        return self.global_time;

    def register_agent(self, sim_obj):
        if not sim_obj.get_create_time() in self.waiting_obj_map:
            self.waiting_obj_map[sim_obj.get_create_time()] = list()

        self.waiting_obj_map[sim_obj.get_create_time()].append(sim_obj)

    def create_agent(self):
        if len(self.waiting_obj_map.keys()) != 0:
            key = min(self.waiting_obj_map)
            if key <= self.global_time:
                lst = self.waiting_obj_map[key]
                for obj in lst:
                    print("global:",self.global_time," create agent:", obj.get_obj_name())
                    self.active_obj_map[obj.get_obj_name()] = obj
                    #self.min_schedule_item.append((obj.time_advance() + self.global_time, obj))
                    self.min_schedule_item.append(obj)
                del self.waiting_obj_map[key]

    def destroy_agent(self):
        if len(self.active_obj_map.keys()) != 0:
            delete_lst = []
            for agent_name, agent in self.active_obj_map.items():
                if agent.get_destruct_time() <= self.global_time :
                    delete_lst.append(agent)

            for agent in delete_lst:
                print("global:",self.global_time," del agent:", agent.get_obj_name())
                del(self.active_obj_map[agent.get_obj_name()])

    def coupling_relation(self, src_obj, out_port, dst_obj, in_port):
        self.port_map[(src_obj, out_port)] = (dst_obj, in_port)

    def output_handling(self, obj, msg):
        if msg is not None:
            destination = self.port_map[(obj, msg.get_dst())]
            if destination == None:
                print("Destination Not Found")
                raise AssertionError


            # Receiver Message Handling
            destination[0].ext_trans(destination[1], msg)
            # Receiver Scheduling
            #self.min_schedule_item.pop()
            #self.min_schedule_item.append((destination[0].time_advance() + self.global_time, destination[0]))

    def init_sim(self):
        self.global_time = min(self.waiting_obj_map)
        for obj in self.active_obj_map.items():
            if obj[1].time_advance() < 0: # exception handling for parent instance
                print("You should override the time_advanced function")
                raise AssertionError
            #self.min_schedule_item.append((obj[1].time_advance() + self.global_time, obj))
            self.min_schedule_item.append(obj)

    def schedule(self):
        # Agent Creation
        self.create_agent()

        # select object that requested minimum time
        self.min_schedule_item = sorted(self.min_schedule_item, key=lambda bm:bm.time_advance())

        tuple_obj = self.min_schedule_item[0]

        while tuple_obj.time_advance() + self.global_time <= self.global_time:
            msg = tuple_obj.output()
            if msg is not None:
                self.output_handling(tuple_obj, msg)

            # Sender Scheduling
            tuple_obj.int_trans()
            #self.min_schedule_item.append((tuple_obj.time_advance() + self.global_time, tuple_obj))
            self.min_schedule_item = sorted(self.min_schedule_item, key=lambda bm:bm.time_advance())
            tuple_obj = self.min_schedule_item[0]

        #self.min_schedule_item.append((tuple_obj.time_advance() + self.global_time, tuple_obj))
        #self.min_schedule_item = sorted(self.min_schedule_item, key=lambda bm: bm.time_advance())

        # update Global Time
        self.global_time += self.time_step

        # Agent Deletion
        self.destroy_agent()

    def simulate(self):
        self.init_sim()
        while len(self.waiting_obj_map) != 0 or len(self.active_obj_map) != 0:
            self.schedule()