"""In this file, we define what set of supplying agents the demanding agent can see."""

__author__ = 'Schasfoort, Abeshzadeh, Broek & Peters'

import random


def subset_traders(demander, randomized_set, observable_set_size):
    total_observable_set = list(randomized_set)
    total_observable_set.remove(demander)
    observable_set = [total_observable_set[i] for i in sorted(random.sample(range(len(total_observable_set)),
                                                                            observable_set_size))]
    return observable_set
