def n(out, arr):
    # Sort the content numerically.
    # If list contains both numbers and non-numbers, sort the non-numbers first.
    non_numbers = list(filter(lambda x: not x.isnumeric(), arr))
    numbers = list(filter(lambda x: x.isnumeric(), arr))
    numbers.sort(key=int)
    non_numbers.sort()
    for s in non_numbers:
        out.append(f"{s}\n")
    for n in numbers:
        out.append(f"{n}\n")
    return out
