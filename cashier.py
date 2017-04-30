import simpy


class Cashier:
    def __init__(self, env, speed):
        self.env = env
        self.speed = speed      # Seconds to checkout one item
        self.resource = simpy.Resource(env, capacity=1)
        self.occupied = False
