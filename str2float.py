# -*- coding: utf-8 -*-
from functools import reduce
import math
DIGITS = {'0': 0, '1': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, '.': -1}

def str2float(s):
    index = s.find('.')  # 从下标0开始，查找在字符串里第一个出现的子串，返回结果：0
    def fn(x, y):
        if y == -1:
            return x
        return x * 10 + y
    # map()函数接收两个参数，一个是函数，一个是Iterable，map将传入的函数依次作用到序列的每个元素，并把结果作为新的Iterator返回
    # reduce把一个函数作用在一个序列[x1, x2, x3, ...]上，这个函数必须接收两个参数，reduce把结果继续和序列的下一个元素做累积计算 
    result = reduce(fn, map(lambda x: DIGITS[x], s)) #使用lambda来创建匿名函数
    return result if index < 0 else result / math.pow(10, len(s) - index - 1)


print('str2float(\'123.456\') =', str2float('123.456'))
if abs(str2float('123.456') - 123.456) < 0.00001:
    print('测试成功!')
else:
    print('测试失败!')