###########################
# 6.0002 Problem Set 1a: Space Cows
# Name:
# Collaborators:
# Time:

from ps1_partition import get_partitions
import time

# ================================
# Part A: Transporting Space Cows
# ================================

# Problem 1


def load_cows(filename):
    """
    Read the contents of the given file.  Assumes the file contents contain
    data in the form of comma-separated cow name, weight pairs, and return a
    dictionary containing cow names as keys and corresponding weights as values.

    Parameters:
    filename - the name of the data file as a string

    Returns:
    a dictionary of cow name (string), weight (int) pairs
    """
    # TODO: Your code here
    records = {}
    with open(filename, "r") as file:
        for line in file:
            line = line.strip()

            # skip empty lines
            if not line:
                continue
            name, weight = line.split(",")
            records[name] = int(weight)
    return records
# Problem 2


cows_list = load_cows("ps1_cow_data.txt")
copy_cows = dict(
    sorted(cows_list.items(), key=lambda item: item[1], reverse=True))
# print(copy_cows)
# print(list(copy_cows))
# b = []
# for cow in list(copy_cows):
#     b.append(cow)
#     if b.__len__() > 5:
#         break
# print(b)


def greedy_cow_transport(cows, limit=10):
    """
    Uses a greedy heuristic to determine an allocation of cows that attempts to
    minimize the number of spaceship trips needed to transport all the cows. The
    returned allocation of cows may or may not be optimal.
    The greedy heuristic should follow the following method:

    1. As long as the current trip can fit another cow, add the largest cow that will fit
        to the trip
    2. Once the trip is full, begin a new trip to transport the remaining cows

    Does not mutate the given dictionary of cows.

    Parameters:
    cows - a dictionary of name (string), weight (int) pairs
    limit - weight limit of the spaceship (an int)

    Returns:
    A list of lists, with each inner list containing the names of cows
    transported on a particular trip and the overall list containing all the
    trips
    """
    # TODO: Your code here
    start = time.time()
    remaining = dict(
        sorted(cows.items(), key=lambda x: x[1], reverse=True)
    )
    trips = []

    while remaining:
        capacity = limit
        trip = []
        for cow, weight in list(remaining.items()):
            if weight <= capacity:
                trip.append(cow)
                capacity -= weight
                del remaining[cow]
        if not trip and remaining:
            print("Cow\\s exceeds spaceship capacity: ")
            print(remaining)
            break
        trips.append(trip)
    end = time.time()
    print(end - start)
    return trips


print("Greedy implementation: ")
print(greedy_cow_transport(cows_list, 10))


# Problem 3
def brute_force_cow_transport(cows, limit=10):
    """
    Finds the allocation of cows that minimizes the number of spaceship trips
    via brute force.  The brute force algorithm should follow the following method:

    1. Enumerate all possible ways that the cows can be divided into separate trips 
        Use the given get_partitions function in ps1_partition.py to help you!
    2. Select the allocation that minimizes the number of trips without making any trip
        that does not obey the weight limitation

    Does not mutate the given dictionary of cows.

    Parameters:
    cows - a dictionary of name (string), weight (int) pairs
    limit - weight limit of the spaceship (an int)

    Returns:
    A list of lists, with each inner list containing the names of cows
    transported on a particular trip and the overall list containing all the
    trips
    """
    # TODO: Your code here
    # eligible_list = {}
    start = time.time()
    best_solution = None
    copy_cows = dict(
        sorted(cows.items(), key=lambda item: item[1], reverse=True))
    for solution in get_partitions(list(copy_cows)):
        valid = True
        for trip in solution:
            trip_weight = sum(copy_cows[cow] for cow in trip)

            if trip_weight > limit:
                valid = False
                break
        if valid:
            if best_solution is None or len(solution) < len(best_solution):
                best_solution = solution
    end = time.time()
    print(end - start)
    return best_solution

    # pass
# Problem 4


print("Brute force implementation: ")
print(brute_force_cow_transport(cows_list, 10))
# for comp_trips in get_partitions(list(copy_cows)):
#     print(comp_trips)


def compare_cow_transport_algorithms():
    """
    Using the data from ps1_cow_data.txt and the specified weight limit, run your
    greedy_cow_transport and brute_force_cow_transport functions here. Use the
    default weight limits of 10 for both greedy_cow_transport and
    brute_force_cow_transport.

    Print out the number of trips returned by each method, and how long each
    method takes to run in seconds.

    Returns:
    Does not return anything.
    """
    # TODO: Your code here
    pass
