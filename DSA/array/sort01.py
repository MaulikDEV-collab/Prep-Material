'''
Search sort01 in code360.
'''

def sortZeroesAndOne(arr, n) :
    i = 0
    j = n-1
    while i<j:
        if arr[i]==0:
            i=i+1
        elif arr[j]==1:
            j=j-1
        else:
            arr[i],arr[j]=arr[j],arr[i]
            i = i+1
            j = j-1
    return arr