def swap_alternate(arr):
    i=0
    while i <= len(arr):
        if i+1 < len(arr):
            arr[i], arr[i+1] = arr[i+1], arr[i]
        i = i + 2
    print(arr)

a = [1,2,3,4,5]
swap_alternate(a)