import simpy
from scipy import stats


class Customer:
    def __init__(self, env, items, speed, cashiers, self_checks, id_num, result_file):
        self.env = env
        self.items = items
        self.speed = speed
        self.destination = None     # Will be a string (I think)
        self.Cashiers = cashiers
        self.Self_Checkouts = self_checks
        self.ID = id_num
        self.Results = result_file

        self.employee_involved = False
        self.kiosk_index = -1
        self.timeArrivedAtLine = 0.0
        self.timeBeginCheckout = 0.0
        self.timeFinished = 0.0

    def decide_destination(self):

        if len(self.Cashiers) is 0:
            self.destination = "self"
            if stats.binom.rvs(n=1, p=.4) == 1:         # 40% of self checkouts involve employee intervention
                self.employee_involved = True
            return
        elif len(self.Self_Checkouts) is 0:
            self.destination = "cashier"
            return

        else:
            if stats.binom.rvs(n=1, p=.25) == 1:        # 25% of people use self checkout
                self.destination = "self"
            else:
                self.destination = "cashier"

        if self.items > 20:
            self.destination = "cashier"
        elif self.items < 5:
            self.destination = "self"

        if self.destination == "self":
            if stats.binom.rvs(n=1, p=.4) == 1:         # 40% of self checkouts involve employee intervention
                self.employee_involved = True

    # NOTE: Requesting the resource for a register is not done here:
    # Once a resource is obtained, Customer calls this to wait
    def checkout(self):
        if self.destination == "cashier":
            yield self.env.timeout((self.items / self.Cashiers[self.kiosk_index].speed) * 60)
        elif self.destination == "self":
            yield self.env.timeout(self.speed * self.items)
            if self.employee_involved:
                yield self.env.timeout(15)          # Approx. 15 second delay if Employee is involved

    def run(self):
        self.timeArrivedAtLine = self.env.now   # Customers immediately queue in a line
        if self.destination == "cashier":
            for i in range(len(self.Cashiers)):     # look for an open kiosk...
                if not self.Cashiers[i].occupied:   # ...if one is found, go there...
                    self.kiosk_index = i
                    break
            if self.kiosk_index < 0:                     # ...if none are open, pick at random
                self.kiosk_index = stats.randint.rvs(0, len(self.Cashiers))

            with self.Cashiers[self.kiosk_index].resource.request() as req:
                yield req
                self.timeBeginCheckout = self.env.now
                self.Cashiers[self.kiosk_index].occupied = True
                yield self.env.process(self.checkout())
                self.timeFinished = self.env.now
                self.Cashiers[self.kiosk_index].occupied = False

        elif self.destination == "self":
            for i in range(len(self.Self_Checkouts)):
                if not self.Self_Checkouts[i].occupied:
                    self.kiosk_index = i
                    break
            if self.kiosk_index < 0:
                self.kiosk_index = stats.randint.rvs(0, len(self.Self_Checkouts))
            with self.Self_Checkouts[self.kiosk_index].resource.request() as req:
                yield req
                self.Self_Checkouts[self.kiosk_index].occupied = True
                self.timeBeginCheckout = self.env.now
                yield self.env.process(self.checkout())
                self.timeFinished = self.env.now
                self.Self_Checkouts[self.kiosk_index].occupied = False

        time_in_line = self.timeBeginCheckout - self.timeArrivedAtLine
        service_time = self.timeFinished - self.timeBeginCheckout
        self.Results.write(str(self.ID) + "," + str(self.items) + "," + self.destination + "," + str(self.kiosk_index)
                           + "," + str(time_in_line) + "," + str(service_time) + "," + str(self.employee_involved) + "\n")
