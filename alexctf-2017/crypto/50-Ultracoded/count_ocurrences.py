#!/usr/bin/python

import sys

nums = [1 if word.lower() == 'one' else 0 for word in open('zero_one').read().split()]

def get_counts(nums):
    counts = []
    last_num = nums[0]
    count = 0
    for num in nums:
        if num != last_num:
            counts.append(count)
            count = 0
        count += 1
        last_num = num
    counts.append(count)
    return counts

def get_decimal(nums):
    result = 0
    for num in reversed(nums):
        result <<= 1
        result += num
    return hex(result)

def get_ascii(nums):
    pass

print len(nums)
#print get_bytes(nums)
#print ''.join(map(str, counts))

