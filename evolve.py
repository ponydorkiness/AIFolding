import time
import os
import random
from collections import deque
from collections.abc import Iterable, Iterator, Sequence
import itertools as it


def sliding_window[T](
        iterable: Iterable[T],
        n: int,
) -> Iterator[tuple[T, ...]]:
    iterator = iter(iterable)
    window = deque(it.islice(iterator, n - 1), maxlen=n)
    for x in iterator:
        window.append(x)
        yield tuple(window)


def rewrite_array(
        lst: list[int],
        pattern: Sequence[int],
        sub: Sequence[int],
) -> list[int]:
    # Reduce non-negative numbers in pattern and substitution
    min_p = min(p for p in pattern if p >= 0)
    pattern = tuple(
        p - min_p if p >= 0 else p
        for p in pattern
    )
    sub = tuple(
        s - min_p if s >= 0 else s
        for s in sub
    )

    match_i = None
    # For each window of the pattern's length
    for i, window in enumerate(sliding_window(lst, len(pattern))):
        # Find how much to reduce non-negative numbers in the window by
        min_w = min(w for w, p in zip(window, pattern) if p >= 0)
        # If the reduced window matches this pattern
        if all(
            w - min_w == p
            for w, p in zip(window, pattern)
            if p >= 0
        ):
            # We have found a match
            match_i = i
            break

    # Return early if a match wasn't found
    if match_i is None:
        return lst

    window = lst[match_i:match_i + len(pattern)]
    wilds = it.compress(window, iter(p < 0 for p in pattern))
    min_repl = min(v for v, p in zip(window, pattern) if p >= 0)
    # Create replacement window (substituting wildcards as needed)
    repl = [
        min_repl + s if s >= 0 else next(wilds)
        for s in sub
    ]

    # Chain items together from before, within, and after the window
    # NOTE The items within the replacement window should be considered
    # "before" the other items for purposes of sorting, so we make each
    # item a tuple with a second value to sort by.
    items = list(it.chain(
        ((v, 1) for v in lst[:match_i]),
        ((v, 0) for v in repl),
        ((v, 1) for v in lst[match_i + len(pattern):]),
    ))
    # Return indices of each item when sorted (1-indexed)
    indices = sorted(range(len(items)), key=items.__getitem__)
    result = [0] * len(indices)
    for new_pos, old_pos in enumerate(indices, 1):
        result[old_pos] = new_pos
    return result
        
def evolve(steps):
    rule1 = [1]
    rule2 = [1]
    start_time = time.time()  # Start timing

    for i in range(1, steps + 1):        
        # Calculate error sum
        rule1score = calculate_error_sum(rule1, 50, False)
        rule2score = calculate_error_sum(rule2, 50, False)
        
        # Print iteration message
        print(f"Iteration {i} training for {round(time.time() - start_time)} seconds")

        # Progress bar
        progress = (i / steps) * 100
        bar = f"[{'#' * (i * 40 // steps)}{' ' * (40 - i * 40 // steps)}] {progress:.2f}%"
        print('\r' + bar)

        if rule1score == 0:
            print(rule1, "0")
            calculate_error_sum(rule2, 50, True)
            return
        rule1 = mutate(rule1)
        rule2 = mutate(rule2)

        if rule1score > rule2score:
            rule1 = rule2
        else:
            rule2 = rule1
    
    print(rule2, rule2score)
    calculate_error_sum(rule2, 50, True)

def calculate_error_sum(mutation, max_tests_per_function, doPrint):
    error_sum = 0
    for i in range(1, max_tests_per_function + 1):  # Start i at 1
        num = decimal_to_map(i)
        target = f(i)
        
        for rule in mutation:
            num = apply_rule(num, rule)
            
        num = map_to_decimal(num)

        error_sum += abs(num - target)
        if doPrint:
            print(f"{i}: {target} => {num}")
    return error_sum

num_of_rules = 5

def apply_rule(array, rule):
    if rule == 1:
        return array
    elif rule == 2:
        pattern = [1, 2]
        sub = [1]
        return rewrite_array(array, pattern, sub)
    elif rule == 3:
        pattern = [1]
        sub = [1,2]
        return rewrite_array(array, pattern, sub)
    elif rule == 4:
        pattern = [1,2,3]
        sub = [1,2]
        return rewrite_array(array, pattern, sub)
    elif rule == 5:
        pattern = [3,1,2]
        sub = [1,2,3]
        return rewrite_array(array, pattern, sub)
    else:
        return array

def mutate(rule_array):
    mutation_type = random.randint(1, 3)
    new_value = random.randint(1, num_of_rules)
    rules = rule_array[:]
    
    if mutation_type == 1:
        rules.append(new_value)
    elif mutation_type == 2 and rules:
        random_index = random.randint(0, len(rules) - 1)
        rules[random_index] = new_value
    elif mutation_type == 3 and len(rules) > 5:
        rules.pop()
    
    return rules

def map_to_decimal(numbers):
    return len(numbers)

def decimal_to_map(num):
    current_list = []
    for i in range(1, num + 1): 
        current_list.append(i)
        current_list = current_list[::-1]
    return current_list

def f(x):
    return x+7

# Example usage
evolve(400)
