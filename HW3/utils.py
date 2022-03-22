from math import sqrt
from typing import List

def normalize(list_of_numbers) -> List[float]:
    '''
    Take a list of numbers and normalize it into unit vector.

    Argument:
        list_of_numbers (List[float]): A list of numbers

    Return:
        Normalized list of numbers
    '''
    total_sum = 0
    for number in list_of_numbers:
        total_sum += number * number
    return list(map(lambda x : x / sqrt(total_sum), list_of_numbers))
