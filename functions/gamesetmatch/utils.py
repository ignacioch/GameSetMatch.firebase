import random

# Generate a random integer and then convert it to hex
def generate_random_hex_int(min_value=0, max_value=0xFFFFFFFF):
    random_int = random.randint(min_value, max_value)
    return hex(random_int)[2:]  # Convert to hex and remove the "0x" prefix
