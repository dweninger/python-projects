import sys
import random

answer = random.randint(1, 100)
print("I'm thinking of a number between 1 and 100.\n"
      "See if you can guess the number in 6 tries.")

for guess_index in range(5, -1, -1):
    user_input = 0
    while True:
        user_input = input("Enter a number between 1 and 100: ")
        try:
            number = int(user_input)
            if 1 <= number <= 100:
                break
            else:
                print("Number must be between 1 and 100. " 
                      "Please try again.")
        except ValueError:
            print("Input is not a valid number. "
                "Please try again.")
    user_guess = int(user_input)
    if user_guess == answer:
        print("Congratulations! " 
              f"Your guess, {user_guess} is the correct number.")
        sys.exit()
    elif user_guess > answer:
        print(f"Sorry! {user_guess} is too high.")
    elif user_guess < answer:
        print(f"Sorry! {user_guess} is too low.")
    print(f"You have {guess_index} guesses remaining")
print(f"Sorry! You lost this round. The number was {answer}.")