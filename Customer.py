import simpy
from scipy import stats


class Customer:
    def __init__(self, env, items, speed, cashiers, self_checks, id_num):
        self.env = env
        self.items = items
        self.speed = speed
        self.destination = None     # Will be a string (I think)
        self.Cashiers = cashiers
        self.Self_Checkouts = self_checks
        self.ID = id_num

        self.employee_involved = False
        self.kiosk_index = -1
        self.timeArrivedAtLine = 0.0
        self.timeBeginCheckout = 0.0
        self.timeFinished = 0.0

        print("CUSTOMER " + str(self.ID) + "\n", str(self.items), str(self.speed), str(len(self.Cashiers)), str(len(self.Self_Checkouts))+"\n")

    def decide_destination(self):
        if self.items > 20:
            self.destination = "cashier"
        elif self.items < 5:
            self.destination = "self"
        else:
            if stats.binom.rvs(n=1, p=.25) == 1:        # 25% of people use self checkout
                self.destination = "self"
            else:
                self.destination = "cashier"

        if self.destination == "self":
            if stats.binom.rvs(n=1, p=.4) == 1:         # 40% of self checkouts involve employee intervention
                self.employee_involved = True

        print("Customer", str(self.ID), "going to", str(self.destination) + "\n")

    # NOTE: Requesting the resource for a register is not done here (or will not be done here):
    # Once a resource is obtained, Customer calls this to wait
    def checkout(self):
        if self.destination == "cashier":
            yield self.env.timeout(self.Cashiers[self.kiosk_index].speed * self.items)
        elif self.destination == "self":
            yield self.env.timeout(self.speed * self.items)
            if self.employee_involved:
                yield self.env.timeout(15)

    def run(self):
        if self.destination == "cashier":
            for i in range(len(self.Cashiers)):     # look for an open kiosk...
                if not self.Cashiers[i].occupied:   # ...if one is found, go there...
                    self.kiosk_index = i
                    break
            # TODO: Maybe change this to pick shortest line?
            if self.kiosk_index < 0:                     # ...if none are open, pick at random
                self.kiosk_index = stats.randint.rvs(0, len(self.Self_Checkouts))

            self.timeArrivedAtLine = self.env.now                             # ?????
            with self.Cashiers[self.kiosk_index].resource.request() as req:
                self.timeBeginCheckout = self.env.now                         # ?????
                print("Customer", str(self.ID), "checking out at cashier", str(self.kiosk_index) + "\n")
                yield self.env.process(self.checkout())
                yield req
                self.timeFinished = self.env.now

        elif self.destination == "self":
            for i in range(len(self.Self_Checkouts)):
                if not self.Self_Checkouts[i].occupied:
                    self.kiosk_index = i
                    break
            # TODO: Maybe change this to pick shortest line?
            if self.kiosk_index < 0:
                self.kiosk_index = stats.randint.rvs(0, len(self.Self_Checkouts))

            self.timeArrivedAtLine = self.env.now                             # ?????
            with self.Cashiers[self.kiosk_index].resource.request() as req:
                self.timeBeginCheckout = self.env.now                         # ?????
                print("Customer", str(self.ID), "checking out at self-check", str(self.kiosk_index)+ "\n")
                yield self.env.process(self.checkout())
                yield req
            self.timeFinished = self.env.now

        print("Customer", self.ID, "Start:" + str(self.timeBeginCheckout) + "End:" + str(self.timeFinished))
