def nr(args, out, arr):
    arr.sort(reverse=True)

    for a in arr:
        out.append(a + "\n")
    
    return out 