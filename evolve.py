import time
import os
import random
from collections import deque
from collections.abc import Iterable, Iterator
import itertools as it
#Sliding_window rewrite_array were written by Josiah Windslow
def sliding_window[T](iterable: Iterable[T], n: int) -> Iterator[tuple[T, ...]]:
    iterator = iter(iterable)
    window = deque(it.islice(iterator, n - 1), maxlen=n)
    for x in iterator:
        window.append(x)
        yield tuple(window)


def rewrite_array(
        lst: list[int],
        pattern: tuple[int, ...],
        sub: tuple[int, ...],
) -> list[int]:
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
    for i, window in enumerate(sliding_window(lst, len(pattern))):
        # Find how much to reduce non-negative numbers in the window by
        min_w = min(w for w, p in zip(window, pattern) if p >= 0)

        match = True
        # Check that the reduced window matches the pattern
        for w, p in zip(window, pattern):
            if p < 0:
                continue
            if w - min_w != p:
                match = False
                break
        if match:
            match_i = i
            break

    if match_i is None:
        return lst

    # Find minimum and maximum values of matched window
    match_window = lst[match_i:match_i + len(pattern)]
    min_w = min(w for w, p in zip(match_window, pattern) if p >= 0)
    max_w = max(match_window)

    # Construct replacement for matched window
    wilds = iter(w for w, p in zip(match_window, pattern) if p < 0)
    repl = [
        min_w + s if s >= 0 else next(wilds)
        for s in sub
    ]

    max_p = max(p for p in pattern if p >= 0)
    max_s = max(s for s in sub if s >= 0)
    # Shift values of other items in list to accomodate replacement
    for i, v in enumerate(lst):
        if v > max_w:
            lst[i] += max_s - max_p

    return lst[:match_i] + repl + lst[match_i + len(pattern):]

def clear_console():
    # Clear command for Windows and UNIX-based systems (Linux, macOS)
    if os.name == 'nt':
        os.system('cls')  # Windows
    else:
        os.system('clear')  # UNIX-based systems
        
def evolve(steps):
    rule1 = [1]
    rule2 = [1]
    start_time = time.time()  # Start timing

    for i in range(1, steps + 1):        
        # Calculate error sum
        rule1score = calculate_error_sum(rule1, 50, False)
        rule2score = calculate_error_sum(rule2, 50, False)
        
        # Print iteration message
        clear_console()
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
