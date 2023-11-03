import numpy as np
from my_sort import InfinitesimalSort


def disorder(arr):
    # Sort the array and create a mapping from value to its sorted position
    sorted_positions = {value: idx for idx, value in enumerate(sorted(arr))}
    
    # Calculate the absolute distance between each element's position and its sorted position
    return [abs(idx - sorted_positions[value]) for idx, value in enumerate(arr)]
    

def measure_disorder(arr):
    distances = disorder(arr)
    # Calculate average, max, and median distance
    average_distance = np.mean(distances)
    max_distance = np.max(distances)
    median_distance = np.median(distances)
    
    return average_distance, max_distance, median_distance


def placeit(slots, idx, ni, direction=None):
    if idx+direction in [-1, len(slots)]:
        direction=-direction
    
    if slots[idx] != 0:
        slots = placeit(slots, idx+direction, ni, direction)
    else:
        slots[idx] = ni
    return slots

def quasi_sort(arr, tresholds= None):
    ''' Uses thresholds to sort the array into slots, if slot occupied, 
    place in next  empsty slot'''
    n = len(arr)
    slots = np.zeros(n)
    if tresholds is None:
        tresholds = InfinitesimalSort().thresholds(n)[1] 

    for ni in arr:
        idx = [ i for i, v in enumerate(np.append([0],tresholds)) if v < ni][-1]

        if slots[idx] != 0:
            if slots[idx] > ni:
                direction = +1
            else:
                direction = -1
            slots = placeit(slots, idx, ni, direction)
        else:
            slots[idx] = ni

    return slots