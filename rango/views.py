from django.shortcuts import render
from django.http import HttpResponse

from rango.models import Category, Page

'''
The functions are called from the urls.py inside the rango app.
'''

# Create your views here.
def index(request):

	'''
	Query the database for a list of all categories currently stored;
	Order the categories by the number of likes in descending order;
	Only retrieve the top 5.
	'''
	category_list = Category.objects.order_by('-likes')[:5]
	page_list = Page.objects.order_by('-views')[:5]

	'''
	Dictionary to pass to the template engine as its context.
	boldmessage matches to {{boldmessage}} in template.
	'''
	context_dict = {}
	context_dict['boldmessage'] = 'Crunchy, creamy, cookie, candy, cupcake!'
	context_dict['categories'] = category_list
	context_dict['pages'] = page_list

	'''
	Return a rendered response to send to the client.
	Make use of the shortcut function to make our lives easier.
	the first parameter is the template we wish to use.

	render will take the template and the context_dict and match [mash] it together
	to produce complete HTML response and returned with HttpResponse.

	'''
	return render(request, 'rango/index.html', context=context_dict)

def about(request):
	context_dict = {'boldmessage':'Dans - 2500414V'}
	return render(request, 'rango/about.html',context=context_dict)

def show_category(request, category_name_slug):

	# Context dictionary passable to the template engine.
	context_dict = {}

	try:

		'''
		Can we find a category name slug with the given name?
		If we cant, the get() throws a DoesNotExist exception.
		The get method returns a single instance.
		'''
		category = Category.objects.get(slug=category_name_slug)

		'''
		Retrieve all of the associated pages for that category.
		The filter() will return a list of Page objects or an empty list.
		'''
		pages = Page.objects.filter(category = category)

		# Add the pages to the template context.
		context_dict['pages'] = pages
		context_dict['category'] = category

	except Category.DoesNotExist:

		'''
		If no category exists, display 'no category message'.
		Essentially, dont do anything.
		'''
		context_dict['category'] = None
		context_dict['pages'] = None

	# Render the response and return to the client.
	return render(request, 'rango/category.html', context_dict)

