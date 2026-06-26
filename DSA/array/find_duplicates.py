'''
https://www.naukri.com/code360/problems/duplicate-in-array_893397
'''
def findDuplicate(arr):
    # Write your code here
    n = len(arr) - 1
    sum = (n*(n+1))//2
    #array sum
    sum_of_array = 0
    for i in arr:
        sum_of_array = sum_of_array + i
    return (sum_of_array - sum)
