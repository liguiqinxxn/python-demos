# -*- coding: utf-8 -*-
class Student(object):
	"""docstring for Student"""
	def __init__(self, name, score):
		self.name = name
		self.score = score

	def get_grade(self):
		if self.score >= 90:
			return 'A'
		elif self.score >= 60:
		    return 'B'
		else:
			return 'C'


lisa = Student('Lisa', 99)
bart = Student('Bart', 59)
print(lisa.name, lisa.get_grade())
print(bart.name, bart.get_grade())