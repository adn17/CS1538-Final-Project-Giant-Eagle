import simpy
import numpy


class Customer:
    def __init__(self, env, items):
        self.env = env
        self.items = items
        self.destination = None

        self.timeArrivedAtLine = 0.0
        self.timeBeginCheckout = 0.0
        self.timeFinished = 0.0

    def decide_destination(self):
        # TODO Decide Destination Based on number of items

    def checkout(self):
        # TODO Wait for time (from distribution, based on type of kiosk)
