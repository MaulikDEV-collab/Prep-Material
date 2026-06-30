'''
You have to find the square root of a number using binary search. The trick is to imagine that lets say for 64 its sqrt will lie bw 0 and 64. Then we check the mid's square if it greater than the number then right =mid-1 else, left =mid+1 and we store that mid in ans, in order to check which ans's square is closest to the target
'''
class Solution:
    def mySqrt(self, x: int) -> int:
        ans = 0
        left = 0
        right = x
        while(left<=right):
            mid = (left+right)//2
            if mid*mid == x:
                return mid
            if mid*mid>x:
                right = mid-1
            elif mid*mid < x:
                left = mid + 1
                if mid > ans: #here we are trying to get as close to the target
                    ans = mid      
        return ans
        