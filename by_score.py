# -*- coding: utf-8 -*-
L = [('Bob', 75), ('Adam', 92), ('Bart', 66), ('Lisa', 88)]
def by_score(t):
	return -t[1]


L2 = sorted(L, key=by_score)
print(L2)