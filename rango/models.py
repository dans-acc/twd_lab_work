from django.db import models

'''
By default, all models have auto-increment integer fields called 'id' - automatically
assigned and acts as primary key.
'''

class Category(models.Model):

	# Every category name must be unique => primary key.
	name = models.CharField(max_length=128,unique=True)
	views = models.IntegerField(default=0)
	likes = models.IntegerField(default=0)

	class Meta:
		verbose_name_plural = 'Categories'

	def __str__(self):
		return self.name

class Page(models.Model):

	'''
	Foreign key allows a one to many relationship with the Category field/model.
	'''
	category = models.ForeignKey(Category, on_delete=models.CASCADE)
	title = models.CharField(max_length=128)
	url = models.URLField()
	views = models.IntegerField(default=0)
	def __str__(self):
		return self.title

