import random

def random_12_digit_number():
    """
    Generate a random integer with exactly 12 digits.
    """
    return random.randint(10**11, 10**12 - 1)

# Example usage:
print(random_12_digit_number())
