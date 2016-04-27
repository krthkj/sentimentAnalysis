#!/usr/bin/env python
import random

def get_state():
    # insert random state
    state_list = ['Alabama','Alaska','Arizona','Arkansas','California','Colorado','Connecticut','Delaware','Florida','Georgia','Hawaii','Idaho','Illinois','Indiana','Iowa','Kansas','Kentucky','Louisiana','Maine','Maryland','Massachusetts','Michigan','Minnesota','Mississippi','Missouri','Montana','Nebraska','Nevada','New Hampshire','New Jersey','New Mexico','New York','North Carolina','North Dakota','Ohio','Oklahoma','Oregon','Pennsylvania','Rhode Island','South Carolina','South Dakota','Tennessee','Texas','Utah','Vermont','Virginia','Washington','West Virginia','Wisconsin','Wyoming']
    return random.choice(state_list)

def get_age():
    # insert random age
    return random.randint(18,60)

def file_array(filename):
    # read file to array
    array = []
    with open (filename) as f:
        for line in f:
            array.append(line.rstrip())

    # print (array)
    return array

