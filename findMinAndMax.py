# -*- coding: utf-8 -*-
def findMinAndMax(L):
	 if L:
	 	min=max=L[0]
	 	for s in L:
	 		if min>s:
	 			min = s
	 		if max<s:
	 			max = s
	 	return (min,max)
	 return (None, None)


# 测试
if findMinAndMax([]) != (None, None):
    print('测试失败!')
elif findMinAndMax([7]) != (7, 7):
    print('测试失败!')
elif findMinAndMax([7, 1]) != (1, 7):
    print('测试失败!')
elif findMinAndMax([7, 1, 3, 9, 5]) != (1, 9):
    print('测试失败!')
else:
    print('测试成功!')