with open("input.txt") as f:
    lines = f.readlines()

import os
from functools import cache
from multiprocessing import Pool

from tqdm import tqdm


def is_valid(s):
    return not ("@#" in s or "#@" in s)


def place_substring(s, length):
    pos = []
    for i in range(len(s) - length + 1):
        # Check for # before
        str_before = s[:i]
        if "#" in str_before:
            return tuple(pos)  # No need to check further
        str_overwritten = s[i : i + length]
        if "." in str_overwritten or "@" in str_overwritten:
            continue
        cur_str = s[:i] + length * "@" + s[i + length :]
        cur_str = cur_str[:i].replace("?", ".") + cur_str[i:]
        if is_valid(cur_str):
            # Replace the chars with '.'
            cur_str = cur_str.replace("@?", "@.").replace("?@", ".@")
            pos.append(cur_str)
    return tuple(pos)


def get_all_pos(s, lengths, total_l):
    if s.count("#") == 0 and s.count("@") == total_l:
        print(f"{s=}")
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
            elif pos.count("#") > sum(lengths_copy):
                continue
            elif (
                pos.count("#") == 0
                and pos.count("@") == total_l
                and len(lengths_copy) == 0
            ):
                total += 1
            elif len(lengths_copy) == 0:
                continue
            elif not can_fit_remaining(pos, lengths_copy):
                continue
            else:
                total += get_all_pos(pos, lengths_copy, total_l)
        return total


def process_example(example):
    return get_all_pos(example[0], tuple(example[1]), sum(example[1]))


def can_fit_remaining(s, lengths):
    s = s.replace("?", "#")
    for l in lengths:
        pos = s.find("#" * l)
        after = s[pos + l :]

        if after.count("#") < sum(lengths) - l:
            return False
    return True


def main():
    examples = []
    for line in lines:
        example = line.strip().split(" ")
        example[0] = "?".join([example[0] for _ in range(5)])
        example[1] = ",".join([example[1] for _ in range(5)])
        example[1] = [int(x) for x in example[1].split(",")]
        examples.append(example)

    with Pool(os.cpu_count()) as pool:
        results = list(
            tqdm(pool.imap_unordered(process_example, examples), total=len(examples))
        )

    total = sum(results)

    len(results)

    print(total)


if __name__ == "__main__":
    main()
