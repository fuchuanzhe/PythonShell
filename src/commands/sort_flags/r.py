def r(out, arr):
    # Reverse the order of the content.
    arr.sort(reverse=True)
    for a in arr:
        out.append(a + "\n")
    return out
