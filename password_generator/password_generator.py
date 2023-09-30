import string
import random

possible_chars = [string.ascii_uppercase, string.ascii_lowercase, string.digits, "!@#$%^&*"]

def get_password(len):
    if not isinstance(len, int) or len < 4:
        return "Password length must be a number greater than 4"
    else:
        random_password = ""
        # Ensure each char type appears at least once in the password
        for char_category in possible_chars:
            random_password += random.choice(char_category)
        remaining_len = len - 4
        for _ in range(remaining_len):
            random_password += random.choice(random.choice(possible_chars))
        random_password_list = list(random_password)
        random.shuffle(random_password_list)
        random_password = ''.join(random_password_list)
        return random_password

password_length = input("Enter password length: ")
print(get_password(password_length))