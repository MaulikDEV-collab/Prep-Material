# def firstAndLastPosition(arr, n, k):

#     def first_occurrence():
#         left, right = 0, n - 1
#         ans = -1

#         while left <= right:
#             mid = (left + right) // 2

#             if arr[mid] == k:
#                 ans = mid
#                 right = mid - 1      # Search on the left
#             elif arr[mid] < k:
#                 left = mid + 1
#             else:
#                 right = mid - 1

#         return ans

#     def last_occurrence():
#         left, right = 0, n - 1
#         ans = -1

#         while left <= right:
#             mid = (left + right) // 2

#             if arr[mid] == k:
#                 ans = mid
#                 left = mid + 1       # Search on the right
#             elif arr[mid] < k:
#                 left = mid + 1
#             else:
#                 right = mid - 1

#         return ans

#     return [first_occurrence(), last_occurrence()]
arr = [0,10,5,2]
max = arr[0]
for i in arr:
    if i > max:
        max = i
        print(max)
left = 0
right = len(arr)-1
while(left <= right):
    mid = (left+right)//2
    if arr[mid] == max:
        print(mid)
    elif arr[mid] > max:
        right = mid-1
    else:
        left = mid + 1
print(mid)