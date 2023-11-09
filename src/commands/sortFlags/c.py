def c(args, out, arr):
    is_sorted = all(a <= b for a, b in zip(arr, arr[1:]))

    if is_sorted:
        print("Yes, the list is sorted.")
    else:
        print("No, the list is not sorted.")
    
    return out 