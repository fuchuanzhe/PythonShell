import sys 

def o(args, out, arr):
    stdout_fileno = sys.stdout
    sys.stdout = open('sorted.txt', 'w')
    arr.sort()
    
    for a in arr:
        sys.stdout.write(a + '\n')
        out.append(a + "\n")
    
    sys.stdout.close()
    sys.stdout = stdout_fileno

    return out 