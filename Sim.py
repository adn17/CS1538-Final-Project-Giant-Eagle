import argparse
import simpy
from scipy import stats
import Customer, cashier, self_checkout


def generate_customers(env):
    customer_id = 0
    while Env.now < sim_seconds:
        customer_items = 10      # TODO Change to random draw based on data
        customer_speed = 5      # TODO Change to random draw based on data
        new_customer = Customer.Customer(Env, customer_items, customer_speed,
                                         Cashiers, Self_Checkouts, customer_id, File)
        new_customer.decide_destination()
        env.process(new_customer.run())
        customer_id += 1
        yield Env.timeout(stats.expon.rvs(loc=2, scale=20))

parser = argparse.ArgumentParser()
parser.add_argument("Cashiers", type=int, help="Number of Cashiers")
parser.add_argument("SelfCheckouts", type=int, help="Number of Self-Checkouts")

args = parser.parse_args()

num_cashiers = args.Cashiers
num_self_checkouts = args.SelfCheckouts
sim_hrs = 12
sim_seconds = sim_hrs * 3600

File = open("Results.csv", "w")
File.write("Customer ID,Number of Items,Kiosk Type,Kiosk Number,Time In Line,Time to Checkout,Employee Involved?\n")    # Top Row

Cashiers = []
Self_Checkouts = []

Env = simpy.Environment()
# Create the Environment
for i in range(num_cashiers):
    Cashiers.append(cashier.Cashier(env=Env, speed=2))  # TODO Change speed to random data based draw

# Generate Resource Objects

for j in range(num_self_checkouts):
    Self_Checkouts.append(self_checkout.Self_Checkout(env=Env))

# Prepare the Generator
Env.process(generate_customers(Env))
# Begin the Simulation (used sim_seconds since everything is on the order of seconds)
Env.run(until=sim_seconds)


