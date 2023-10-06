import random

def generate_random_number(lower_bound, upper_bound):
    if upper_bound <= lower_bound:
        print("Upper bound must be greater "
              "than the lower bound.")
        return None
    return random.randint(lower_bound, upper_bound)

print("Welcome to the Random Number Generator!")
lower_bound = int(input("Enter the lower bound: "))
upper_bound = int(input("Enter the upper bound: "))

while True:
    random_number = generate_random_number(
        lower_bound, 
        upper_bound)
    if random_number is not None:
        print(f"Random number between "
              f"{lower_bound} and {upper_bound}: "
              f"{random_number}")

    play_again = input(
        "Generate another random number? (yes/no): ").lower()
    if play_again != "yes":
        break
