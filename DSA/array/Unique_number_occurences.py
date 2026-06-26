'''
Search for in leetcode with same name
'''
from typing import List

class Solution:
    def uniqueOccurrences(self, arr: List[int]) -> bool:
          #first lets make a hash map to check counter for each value
        freq = {}
        for num in arr:
            freq[num] = freq.get(num, 0) + 1
         #lets make a set now
        seen = set()
        #here we are checking if the set is unique 
        for i in freq.values:
            if i in seen:
                return False
            seen.add(i)
        
        return True
