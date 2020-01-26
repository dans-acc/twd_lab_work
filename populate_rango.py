import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tango_with_django_project.settings')

import django

'''
When importing models, set/import the DJANGO_SETTINGS_MODULE path i.e. import settings.py.
django.setup() imports the settings.
'''
django.setup()

'''
Imported after the setting of the django environment and importing settings.
Doing this before would result in an exception!
'''
from rango.models import Category, Page

def populate():

	# First, create lists of directories containing the pages
	# we want to add into each category.
	# Then create a ductionary of dictionaries for our categories.

	python_pages = [ 
	{'title': 'Official Python Tutorial','url':'http://docs.python.org/3/tutorial/'},
	{'title': 'How to Think like a Computer Scientist', 'url': 'http://www.greenteapress.com/thinkpython/'},
	{'title': 'Learn Python in 10 Minutes', 'url':'http://www.korokithakis.net/tutorials/python/'}
	]

	django_pages = [
	{'title': 'Official Django Tutorial','url':'https://docs.djangoproject.com/en/2.1/intro/tutorial01/'},
	{'title': 'Django Rocks', 'url': 'http://www.djangorocks.com/'},
	{'title': 'How to Tango with Django', 'url':'http://www.tangowithdjango.com/'}
	]

	other_pages = [
	{'title': 'Bottle','url':'http://bottlepy.org/docs/dev/'},
	{'title': 'Flask', 'url': 'http://flask.pocoo.org'}
	]

	cats = {
	'Python': {'pages': python_pages, 'views': 128, 'likes': 64},
	'Django': {'pages': django_pages, 'views': 64, 'likes': 32},
	'Other Frameworks': {'pages': other_pages, 'views': 32, 'likes': 16}
	}

	# Loops through cats, adds each category and then each associated page.
	for cat, cat_data in cats.items():
		c = add_cat(cat, cat_data['views'], cat_data['likes'])
		for page in cat_data['pages']:
			add_page(c, page['title'], page['url'])

	# Print out all the categories we have added.
	for c in Category.objects.all():
		for p in Page.objects.filter(category = c):
			print(f'- {c}: {p}')

def add_page(cat, title, url, views = 0):
	
	# Use get_or_create so as to not create duplicates in the database.
	# Returns a tuple (object, created) => object is the model instance (created or found), created denoted
	# whether the model was returned or created.
	
	p = Page.objects.get_or_create(category=cat, title=title)[0]
	p.url = url
	p.views = views
	p.save()
	return p

def add_cat(name, views=0, likes=0):
	c = Category.objects.get_or_create(name=name)[0]
	c.views = views 
	c.likes = likes
	c.save()
	return c

'''
Starts the execution here.

__name__ == '__main__' allows the python module to act as either reusable module or a standalone
python script.

Code inside __name__ == '__main__' will only execute when the script is run as a standalone module.
Importing this module will not run this code.
'''
if __name__ == '__main__':
	print('Starting Rango population script...')
	populate()




