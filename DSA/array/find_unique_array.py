'''
Question: find the unique number in a list when other numbers are repeated twice in the list.

The idea behind this solution is that in order to find the unique number you can xor all the items in the array
and if same numbers are XOR their output is 0. And, 0^a = a. a^a=0.
'''

from typing import List


class Solution:
    def singleNumber(self, nums: List[int]) -> int:
        ans = 0
        for i in nums:
            ans = ans^i
        return ans
    