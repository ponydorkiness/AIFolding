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
        apply_once: bool = False,
) -> list[int]:
    # Reduce non-negative numbers in pattern and substitution
    min_p = min((p for p in pattern if p >= 0), default=None)
    if min_p is not None:
        pattern = tuple(
            p - min_p if p >= 0 else p
            for p in pattern
        )
        sub = tuple(
            s - min_p if s >= 0 else s
            for s in sub
        )
    else:
        # We should not be replacing wildcard-only patterns with
        # anything containing non-wildcards
        assert all(s < 0 for s in sub)

    matches = []
    i = 0
    while i + len(pattern) <= len(lst):
        window = lst[i:i + len(pattern)]
        min_w = min(
            (w for w, p in zip(window, pattern) if p >= 0),
            default=0,
        )
        if all(
            w - min_w == p
            for w, p in zip(window, pattern)
            if p >= 0
        ):
            matches.append(i)
            if apply_once:
                break
            i += len(pattern)
            continue
        i += 1

    # If no matches were found, return the original list
    if not matches:
        return lst

    result = lst.copy()
    for match_i in reversed(matches):
        window = result[match_i:match_i + len(pattern)]
        wilds = {p: v for v, p in zip(window, pattern) if p < 0}
        min_repl = min(
            (v for v, p in zip(window, pattern) if p >= 0),
            default=0,
        )
        repl = [
            min_repl + s if s >= 0 else wilds[s]
            for s in sub
        ]

        items = list(it.chain(
            ((v, 1) for v in result[:match_i]),
            ((v, 0) for v in repl),
            ((v, 1) for v in result[match_i + len(pattern):]),
        ))
        indices = sorted(range(len(items)), key=items.__getitem__)
        result = [0] * len(indices)
        for new_pos, old_pos in enumerate(indices, 1):
            result[old_pos] = new_pos

        if apply_once:
            break

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
        print(f"Iteration {i} training for {round(time.time() - start_time)} seconds - The current score is {rule2score}")
        
        # Progress bar
        progress = (i / steps) * 100
        bar = f"[{'#' * (i * 40 // steps)}{' ' * (40 - i * 40 // steps)}] {progress:.2f}%"
        print(bar)

        if rule1score == 0:
            print("\n", rule1, "0")
            calculate_error_sum(rule2, 50, True)
            return

        # Mutate rules
        rule1 = mutate(rule1)
        rule2 = mutate(rule2)

        # Occasionally choose randomly instead of by score
        if random.random() < 0.2:  # 20% chance to mutate randomly.
            if random.choice([True, False]):
                rule1 = rule2
            else:
                rule2 = rule1
        else:  # Default to choosing the mutation with the lower score
            if rule1score > rule2score:
                rule1 = rule2
            else:
                rule2 = rule1

    print("\n", rule2, rule2score)
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

rules = {
    #Pattern, Subsiution, Match only first occurrence?
    1: ([1], [1], True), 
    2: ([1, 2], [1], True),
    3: ([1], [1, 2], True), 
    4: ([1,2,3], [1, 2], True), 
    5: ([3,1,2], [1, 2, 3], True), 
    7: ([-1,-2,-3, 1], [-3, -2, -1, 1, 2], False), 
    8: ([1, 2], [1], False),
    9: ([1], [1, 2], False), 
    10: ([1,2,3], [1, 2], False), 
    11: ([3,1,2], [1, 2, 3], False), 
}
num_of_rules = len(rules)

def apply_rule(array, rule):
    if rule in rules:
        pattern, sub, PickFirst = rules[rule]
        return rewrite_array(array, pattern, sub, PickFirst)
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
    return x*3

# Example usage
evolve(400)
