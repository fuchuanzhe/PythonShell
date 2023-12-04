def n(args, out, arr):
    # Sort the content numerically.
    arr.sort()
    for a in arr:
        out.append(a + "\n")
    return out
