import string
import random

def id_generator(n, chars=string.ascii_uppercase + string.ascii_lowercase+ string.digits):
    return ''.join(random.choice(chars) for _ in range(n))

def id_generator_digits(n, chars=string.digits):
    return ''.join(random.choice(chars) for _ in range(n))
