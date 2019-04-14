import random
from functools import wraps

def get_rnd_step(step, max):
    return random.choice(range(1, int(max) + 1, step))
