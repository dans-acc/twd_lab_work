from django.shortcuts import render, redirect, reverse
from django.http import HttpResponse

from rango.models import Category, Page
from rango.forms import CategoryForm, PageForm

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

'''
Handles:
    Showing a new blank form for adding a category.
    Saving data provided by the user to the associated model and redirecting to the homepage.
    Display any errors that may have occurred.
'''
def add_category(request):

	# First we create a category form.
	form = CategoryForm()

	# A HTTP POST i.e. did the user submit data via the form.
	# We can handle the POST request through the same URL.
	if request.method == 'POST':
		form = CategoryForm(request.POST)

		# Have we been provided with a valid form
		if form.is_valid():
			
			# Save the new category to the database.
			form.save(commit=True)

			# Now that the category is saved, we could confirm this.
			# For now, redirect the user back to the index page.
			return redirect('/rango/')
		else:

			# The supplied form contains errors.
			# Print them to the terminal.
			print(form.errors)

	# Will handle bad form, new form, or no form.
	# Render the form with error messages - if any.
	return render(request, 'rango/add_category.html', {'form': form})

def add_page(request, category_name_slug):

	# Get the category from the database.
	try:
		category = Category.objects.get(slug=category_name_slug)
	except Category.DoesNotExist:
		category = None

	# You cannot add a page to a category that does not exist.
	if category is None:
		return redirect('/rango/')

	form = PageForm()

	if request.method == 'POST':
		form = PageForm(request.POST)
		if form.is_valid():
			if category:
				page = form.save(commit = False)
				page.category = category
				page.views = 0
				page.save()

				# Redirect the user to the show_category page once the page has been created.
				# Reverse function is used to look up the URL name in urls.py (rango:show_category)
				# The dictionary provides a means of passing a parameter to the page.
				return redirect(reverse('rango:show_category', kwargs={'category_name_slug': category_name_slug}))
		else:
			print(form.errors)

	context_dict = {'form': form, 'category': category}
	return render(request, 'rango/add_page.html', context = context_dict)

