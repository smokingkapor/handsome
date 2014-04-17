# -*- coding: utf-8 -*-
import random
import string


def generate_str(length):
    seed = string.lowercase + string.digits
    result = []
    for i in range(length):
        result.append(random.choice(seed))
    return ''.join(result)
