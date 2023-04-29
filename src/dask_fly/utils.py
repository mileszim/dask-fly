import random
import string

def random_string():
    return ''.join(random.sample(string.ascii_lowercase+string.digits, 10))
