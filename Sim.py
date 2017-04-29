import argparse
import numpy
import simpy
from scipy import stats
import Customer, cashier, self_checkout


# Items are distributed bimodally; people are equally likely to come in for just a few things (~<10) as for many (~<35)
def generate_items():
    if stats.binom.rvs(1, .5) == 1:
        items = stats.norm.rvs(loc=24, scale=5.56)
    else:
        items = stats.norm.rvs(loc=4.2, scale=2.5)
        if items < 1:
            items = 1
    return round(items, 0)


def generate_customers(env):
    customer_id = 0
    while Env.now < sim_seconds:
        customer_items = generate_items()
        customer_speed = stats.expon.rvs(loc=15, scale=20.4)
        new_customer = Customer.Customer(Env, customer_items, customer_speed,
                                         Cashiers, Self_Checkouts, customer_id, File)
        new_customer.decide_destination()
        env.process(new_customer.run())
        customer_id += 1
        yield Env.timeout(stats.expon.rvs(loc=2, scale=20))

parser = argparse.ArgumentParser()
parser.add_argument("Cashiers", type=int, help="Number of Cashiers")
parser.add_argument("SelfCheckouts", type=int, help="Number of Self-Checkouts")
parser.add_argument("-Days", type=int, help="Number of (10-hour) days to run", default=1, required=False)

args = parser.parse_args()

num_cashiers = args.Cashiers
num_self_checkouts = args.SelfCheckouts
sim_hrs = 10 * args.Days
sim_seconds = sim_hrs * 3600

numpy.random.seed(4321)

File = open("Results.csv", "w")
File.write("Customer ID,Number of Items,Kiosk Type,Kiosk Number,Time In Line,Time to Checkout,Employee Involved?\n")

Cashiers = []
Self_Checkouts = []

Env = simpy.Environment()
# Create the Environment
for i in range(num_cashiers):
    Cashiers.append(cashier.Cashier(env=Env, speed=stats.expon.rvs(loc=15, scale=5.2)))

# Generate Resource Objects

for j in range(num_self_checkouts):
    Self_Checkouts.append(self_checkout.Self_Checkout(env=Env))

# Prepare the Generator
Env.process(generate_customers(Env))
# Begin the Simulation (used sim_seconds since everything is on the order of seconds)
Env.run(until=sim_seconds)


