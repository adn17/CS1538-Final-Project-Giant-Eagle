import simpy
import numpy


class Customer:
    def __init__(self, env, items, cashiers, self_checks, id_num):
        self.env = env
        self.items = items
        self.destination = None     # Will be a string (I think)
        self.Cashiers = cashiers
        self.Self_Checkouts = self_checks
        self.ID = id_num

        self.timeArrivedAtLine = 0.0
        self.timeBeginCheckout = 0.0
        self.timeFinished = 0.0

    def decide_destination(self):
        # TODO Decide Destination Based on number of items
        None

    # NOTE: Requesting the resource for a register is not done here (or will not be done here):
    # Once a resource is obtained, Customer calls this to wait
    def checkout(self):
        if self.destination == "cashier":
            # TODO Wait for a time (numer of items * cashier speed)
            None
        elif self.destination == "self":
            # TODO Wait for time (number of items * customer self-checkout speed [or however this is done])
            None

    def run(self):
        kiosk_index = -1
        if self.destination == "cashier":
            for i in range(len(self.Cashiers)):     # look for an open kiosk...
                if not self.Cashiers[i].occupied:   # ...if one is found, go there...
                    kiosk_index = i
                    break
            # TODO: Maybe change this to pick shortest line?
            if kiosk_index < 0:                     # ...if none are open, pick at random
                kiosk_index = numpy.random.randint(0, len(self.Self_Checkouts)-1)

            # self.timeArrivedAtLine = self.env.now() (???)
            with self.Cashiers[kiosk_index].resource.request() as req:
                # self.timeBeginCheckout = self.env.now()
                yield self.env.process(self.checkout())
                yield req

        elif self.destination == "self":
            for i in range(len(self.Self_Checkouts)):
                if not self.Self_Checkouts[i].occupied:
                    kiosk_index = i
                    break
            # TODO: Maybe change this to pick shortest line?
            if kiosk_index < 0:
                kiosk_index = numpy.random.randint(0, len(self.Self_Checkouts)-1)

            # self.timeArrivedAtLine = self.env.now() (???)
            with self.Cashiers[kiosk_index].resource.request() as req:
                # self.timeBeginCheckout = self.env.now()
                yield self.env.process(self.checkout())
                yield req
