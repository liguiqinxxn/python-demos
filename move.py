# -*- coding: utf-8 -*-
def move(n, a, b, c):
    if n == 1:
        print(a, '-->', c)
    elif n == 2:
        print(a, '-->', b)
        print(a, '-->', c)
        print(b, '-->', c)
    else:
        move(n - 1, a, c, b)    # 先把n-1个盘子移到B
        print(a, '-->', c)        # 把最底下的移到C
        move(n - 2, b, c, a)    # 把B上的n-2个移回A，留下一个
        print(b, '-->', c)        # 把B上的一个移到C
        move(n - 2, a, b, c)    # 这样问题就由之前的移动A上n个盘子到C变成了移动n-2个

# 期待输出:
# A --> C
# A --> B
# C --> B
# A --> C
# B --> A
# B --> C
# A --> C
move(3, 'A', 'B', 'C')
# move(4, 'A', 'B', 'C')
# move(5, 'A', 'B', 'C')
# move(6, 'A', 'B', 'C')