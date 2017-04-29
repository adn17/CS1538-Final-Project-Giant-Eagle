import simpy
from scipy import stats
import Customer, cashier, self_checkout


def generate_customers(env):
    customer_id = 0
    while Env.now < sim_seconds:
        customer_items = 10      # TODO Change to random draw based on data
        customer_speed = 5      # TODO Change to random draw based on data
        new_customer = Customer.Customer(Env, customer_items, customer_speed, Cashiers, Self_Checkouts, customer_id)
        new_customer.decide_destination()
        env.process(new_customer.run())
        customer_id += 1
        yield Env.timeout(20)   # TODO Change to random draw based on data


# TODO Parse arguments from command line:
#   -Number of Cashiers
#   -Number of Self-Checkouts
#   -How Long to run for??? Unless it just runs for a whole day (this will likely be in hours)

num_cashiers = 5
num_self_checkouts = 5
sim_hrs = 3
sim_seconds = sim_hrs * 3600

Cashiers = []
Self_Checkouts = []

Env = simpy.Environment()
# Create the Environment
for i in range(num_cashiers):
    Cashiers.append(cashier.Cashier(env=Env, speed=2))


# Generate Resource Objects

for i in range(num_self_checkouts):
    Self_Checkouts.append(self_checkout.Self_Checkout(env=Env))

# Prepare the Generator
Env.process(generate_customers(Env))
# Begin the Simulation (used sim_seconds since everything is on the order of seconds)
Env.run(until=sim_seconds)
