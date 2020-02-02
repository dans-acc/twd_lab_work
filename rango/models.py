from django.db import models
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify

'''
By default, all models have auto-increment integer fields called 'id' - automatically
assigned and acts as primary key.
'''

class Category(models.Model):

	NAME_MAX_LENGTH = 128

	# Every category name must be unique => primary key.
	name = models.CharField(max_length=NAME_MAX_LENGTH,unique=True)
	views = models.IntegerField(default=0)
	likes = models.IntegerField(default=0)
	slug = models.SlugField(unique=True)

	class Meta:
		verbose_name_plural = 'Categories'

	'''
	The slug field will be updated when the model is saved to reflect a slug version of the name.
	Then the overriden method calls the parent save method defined in the base django.db.models.Model class.
		Parent save saves the changes to the database.
	'''
	def save(self, *args, **kwargs):
		self.slug = slugify(self.name)
		super(Category, self).save(*args, **kwargs)

	def __str__(self):
		return self.name

class Page(models.Model):

	TITLE_MAX_LENGTH = 128
	URL_MAX_LENGTH = 200

	'''
	Foreign key allows a one to many relationship with the Category field/model.
	'''
	category = models.ForeignKey(Category, on_delete=models.CASCADE)
	title = models.CharField(max_length=TITLE_MAX_LENGTH)
	url = models.URLField()
	views = models.IntegerField(default=0)
	def __str__(self):
		return self.title

class UserProfile(models.Model):

	# This line is required as it links UserProfile to a User model instance.
	# Note that we are referencing the User model defined in: django.contrib.auth.models.
	# We want to make this association when we register the user.
	user = models.OneToOneField(User, on_delete=models.CASCADE)

	# The additional attributes we wish to include; blank=True means user does not need to specify.
	website = models.URLField(blank=True)

	# upload_to is conjoined with the projects MEDIA_ROOT setting to provide a path with which to uploaded profilei images.
	# ... will be stored e.g. <workspace>/tango_with_django_project/media/profile_images/
	picture = models.ImageField(upload_to='profile_images', blank=True)

	def __str__(self):
		return self.user.username



