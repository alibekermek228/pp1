def has_33(nums):
    d = [i for i, el in enumerate(nums) if el==3]
    for i in range(len(d)-1):
        if d[i+1]-d[i] == 1:
            return True
    return False
# def has_33(nums):
#     for i in range(len(nums) - 1):
#         if nums[i] == 3 and nums[i + 1] == 3:
#             return True
#     return False


has_33([1, 3, 3])
has_33([1, 3, 1, 3])
has_33([3, 1, 3])

# print(has_33([1, 3, 3]))
# print(has_33([1, 3, 1, 3]))
# print(has_33([3, 1, 3]))