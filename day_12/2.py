# %%
with open("input.txt") as f:
    lines = f.readlines()

# %%
from functools import cache


# %%
def is_valid(s):
    if "@#" in s or "#@" in s:
        return False
    else:
        return True


# %%
def place_substring(s, length):
    pos = []
    for i in range(len(s) - length + 1):
        str_overwritten = s[i : i + length]
        if "." in str_overwritten or "@" in str_overwritten:
            continue
        # Check for # before
        for j in range(i - 1):
            if s[j] == "#":
                return tuple(pos)  # No need to check further
        cur_str = s[:i] + length * "@" + s[i + length :]
        for j in range(i):
            if cur_str[j] == "?":
                cur_str = cur_str[:j] + "." + cur_str[j + 1 :]

        if is_valid(cur_str):
            # Replace the chars with '.'
            cur_str = cur_str.replace("@?", "@.").replace("?@", ".@")
            pos.append(cur_str)
    return tuple(pos)


# %%
def get_all_pos(s, lengths, total_l):
    if s.count("#") == 0 and s.count("@") == total_l:
        return 1
    if len(lengths) == 0:
        return 0
    else:
        lengths_copy = lengths
        next_poss = place_substring(s, lengths_copy[0])
        lengths_copy = lengths_copy[1:]
        total = 0
        for pos in next_poss:
            # Check first if it could even be a solution:
            if pos.count("#") + pos.count("@") > total_l:
                continue
            elif pos.count("#") + pos.count("?") < sum(lengths_copy):
                continue
            else:
                total += get_all_pos(pos, lengths_copy, total_l)
        return total


# %%
examples = []
for line in lines:
    example = line.strip().split(" ")
    example[0] = "?".join([example[0] for _ in range(5)])
    example[1] = ",".join([example[1] for _ in range(5)])
    example[1] = [int(x) for x in example[1].split(",")]
    examples.append(example)


# %%
def process_example(example):
    return get_all_pos(example[0], tuple(example[1]), sum(example[1]))


import os
from multiprocessing import Pool

# %%
from tqdm import tqdm

# Assuming 'examples' is a list of tuples
with Pool(os.cpu_count()) as pool:
    results = list(tqdm(pool.imap(process_example, examples), total=len(examples)))

total = sum(results)


# %%
len(results)

# %%
print(total)

# %%
7007, 322723, 46660346
