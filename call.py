# -*- coding: utf-8 -*-
def call(func):
	def wrapper(*args,**kw):
		print('begin call')
		func(*args,**kw)
		print('end call')
		return func(*args,**kw)
	return wrapper

# 测试
@call
def add(x,y):
	return x+y;
f = add(11, 22)
if f !=33:
	print('测试失败！')