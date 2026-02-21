###########################
# 6.0002 Problem Set 1b: Space Change
# Name:
# Collaborators:
# Time:
# Author: charz, cdenise

# ================================
# Part B: Golden Eggs
# ================================

# Problem 1


def dp_make_weight(egg_weights, target_weight, memo=None):
    """
    Find number of eggs to bring back, using the smallest number of eggs. Assumes there is
    an infinite supply of eggs of each weight, and there is always a egg of value 1.

    Parameters:
    egg_weights - tuple of integers, available egg weights sorted from smallest to largest value (1 = d1 < d2 < ... < dk)
    target_weight - int, amount of weight we want to find eggs to fit
    memo - dictionary, OPTIONAL parameter for memoization (you may not need to use this parameter depending on your implementation)

    Returns: int, smallest number of eggs needed to make target weight
    """
    # TODO: Your code here
    result = [0, 0, []]
    if target_weight <= 0 or len(egg_weights) <= 0:
        return result
    # memo check
    if memo is None:
        memo = {}

    if (egg_weights, target_weight) in memo:
        return memo[(egg_weights, target_weight)]
    least_branch = 0
    for egg in egg_weights:
        branch_result = [0, 0, []]
        if egg > target_weight:
            # Do something
            newList = list(egg_weights)
            newList.remove(egg)
            new_egg_weights = tuple(newList)
            branch_result = dp_make_weight(
                new_egg_weights, target_weight, memo)
        else:
            # Do another thing
            branch_result = [1, egg, [egg,]]
            rec_result = dp_make_weight(egg_weights, target_weight - egg, memo)
            branch_result[0] = branch_result[0] + rec_result[0]
            branch_result[1] = branch_result[1] + rec_result[1]
            branch_result[2] = branch_result[2] + rec_result[2]

        if branch_result[0] < least_branch or least_branch == 0:
            least_branch = branch_result[0]
            result = branch_result
            memo[(egg_weights, target_weight)] = result
    return result


def dp_make_weight_smart(egg_weights, target_weight, memo=None):
    if (memo == None):
        memo = {}
    # Base case: exact match
    if target_weight == 0:
        return [0, 0, []]
    # Base case: Impossible
    if target_weight < 0:
        return None
    # Memo check
    if (target_weight in memo):
        return memo[target_weight]

    best_solution = None
    for egg in egg_weights:
        # result = [0, 0, []]
        if egg <= target_weight:
            sub_result = dp_make_weight(egg_weights, target_weight - egg, memo)
            # sanity check
            if sub_result is not None:
                count = 1 + sub_result[0]
                total_weight = egg + sub_result[1]
                egg_list = [egg] + sub_result[2]

                candidate = [count, total_weight, egg_list]
                # compare
                if best_solution == None or count < best_solution[0]:
                    best_solution = candidate

    return best_solution


# EXAMPLE TESTING CODE, feel free to add more if you'd like
def dp_make_weight_bottom_up(egg_weights, target_weight):
    dp = [None] * (target_weight + 1)
    dp[0] = [0, 0, []]

    for w in range(1, target_weight + 1):
        best_solution = None
        for egg in egg_weights:
            if egg <= w and dp[w-egg] != None:
                prev = dp[w-egg]
                candidate = [prev[0] + 1, prev[1] + egg, prev[2] + [egg]]
            if best_solution == None or candidate[0] < best_solution[0]:
                best_solution = candidate
        dp[w] = best_solution
    return dp[target_weight]


if __name__ == '__main__':
    egg_weights = (1, 5, 10, 25, 121, 567, 2, 56, 2, 7)
    n = 1971
    print("Egg weights = (1, 4, 10, 25)")
    print("n = 99")
    print("Expected ouput: 9 (3 * 25 + 2 * 10 + 4 * 1 = 99)")
    print("Actual output:", dp_make_weight_bottom_up(egg_weights, n))

    # for egg in list(egg_weights):
    #     print(egg)

    print()
    # print(dp_make_weight(egg_weights, 99, {}))
