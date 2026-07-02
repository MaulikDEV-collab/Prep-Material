#check out 1552. Magnetic Force Between Two Balls in Leetcode

def isPossible(position: List[int], m: int, mid: int):
    cows_count = 1
    last_position = position[0]
    for i in position:
        if i - last_position >= mid:
            last_position = i
            cows_count += 1
        if cows_count == m:
            return True
    return False

class Solution:
    def maxDistance(self, position: List[int], m: int) -> int:
        ans = -1
        low = 1
        position.sort()
        high = position[-1]
        while(low<=high):
            mid = (low+high)//2
            #if solution is possible
            if (isPossible(position, m, mid)):
                ans = mid
                low = mid + 1
            else:
                high = mid - 1
        return ans 