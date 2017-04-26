import simpy


class Self_Checkout:
    def __init__(self, env):
        self.env = env
        self.resource = simpy.Resource(env, capacity=1)
        self.occupied = False
