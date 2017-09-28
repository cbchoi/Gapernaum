# simulation structure

class SimObject:
    INIT = 0
    def __init__(self, time):
        self.instance_t = time
        self.state = SimObject.INIT

    def next_event(self):
        return -1


class SimEngine:
    def __init__(self):
        self.global_time = 0
        self.object_map = {}

    # retrive global time
    def get_global_time(self):
        return self.global_time;

    def register_agent(self, sim_obj, user_id=-1):
        if user_id == -1:
            self.object_map[len(self.object_map)] = sim_obj
        else:
            self.object_map[user_id] = sim_obj

    def schedule(self):
        min_schedule_tiem = list()
        for obj in self.object_map.items():
            min_schedule_tiem.append((obj[1].next_event(), obj))
        min_schedule_tiem.sort()
