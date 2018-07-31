# -*- coding: utf-8 -*-
import functools

def log(text):
    if isinstance(text,str):
        def decorator(func):
            @functools.wraps(func)
            def wrapper(*args, **kw):
                print('%s %s():' % (text, func.__name__))
                return func(*args,**kw)
            return wrapper
        return decorator
    else:
        @functools.wraps(text)
        def wrapper(*args, **kw):
            print('call %s():' % text.__name__)
            return text(*args, **kw)
        return wrapper

@log
def now():
    print('2018-6-12')
now()

@log('execute')
def then():
    print('then print')
then()