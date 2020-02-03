from django.shortcuts import render, redirect, reverse
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from rango.models import Category, Page
from rango.forms import CategoryForm, PageForm, UserForm, UserProfileForm

from datetime import datetime

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


	visitor_cookie_handler(request)
	# context_dict['visits'] = int(request.session['visits'])

	'''
	Set a test cookie
	request.session.set_test_cookie()
	'''

	'''
	Return a rendered response to send to the client.
	Make use of the shortcut function to make our lives easier.
	the first parameter is the template we wish to use.

	render will take the template and the context_dict and match [mash] it together
	to produce complete HTML response and returned with HttpResponse.
	'''
	response = render(request, 'rango/index.html', context=context_dict)
	return response

# Server side cookie helper function.
def get_server_side_cookie(request, cookie, default_val=None):
	val = request.session.get(cookie)
	if not val:
		val = default_val
	return val

def visitor_cookie_handler(request):

	# Get the number of visits to the site.
	# We use COOKIES.get() to obtain the visits cookie.
	# If it exists, cast to integer, otherwise default to 1.
	visits = int(get_server_side_cookie(request, 'visits', '1'))

	last_visit_cookie = get_server_side_cookie(request, 'last_visit', str(datetime.now()))
	last_visit_time = datetime.strptime(last_visit_cookie[:-7], '%Y-%m-%d %H:%M:%S')

	# If it's been more than a day since the last visit...
	if (datetime.now() - last_visit_time).days > 0:
		visits = visits + 1

		# Update the last visit cookie now that we have updated the count.
		request.session['last_visit'] = str(datetime.now())
	else:

		# Set the last visit cookie.
		request.session['last_visit'] = last_visit_cookie

	# Update/set the visits cookie.
	request.session['visits'] = visits

'''
def visitor_cookie_handler(request, response):

	# Get the number of visits to the site.
	# We use COOKIES.get() to obtain the visits cookie.
	# If it exists, cast to integer, otherwise default to 1.
	visits = int(request.COOKIES.get('visits', '1'))

	last_visit_cookie = request.COOKIES.get('last_visit', str(datetime.now()))
	last_visit_time = datetime.strptime(last_visit_cookie[:-7], '%Y-%m-%d %H:%M:%S')

	# If it's been more than a day since the last visit...
	if (datetime.now() - last_visit_time).days > 0:
		visits = visits + 1

		# Update the last visit cookie now that we have updated the count.
		response.set_cookie('last_visit', str(datetime.now()))
	else:

		# Set the last visit cookie.
		response.set_cookie('last_visit', last_visit_cookie)

	# Update/set the visits cookie.
	response.set_cookie('visits', visits)
'''


def about(request):

	'''
	# Check for the test cookie and then delete it.
	if request.session.test_cookie_worked():
		print('TEST COOKIE WORKED')
		request.session.delete_test_cookie()
	'''

	visitor_cookie_handler(request)

	context_dict = {'boldmessage':'Dans - 2500414V', 'visits': int(request.session['visits'])}
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
@login_required
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

@login_required
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

def register(request):

	# A boolean value for denoting whether or not registration was successful.
	registered = False

	# If the method is POST we are interested in processing form data.
	if request.method == 'POST':

		# Attempt to grab information from the raw form data.
		# Note that we make use of both the UserForm and UserProfileForm
		user_form = UserForm(request.POST)
		profile_form = UserProfileForm(request.POST)

		# If the two forms are valid...
		if user_form.is_valid() and profile_form.is_valid():

			# Save the users form data to the database.
			user = user_form.save()

			# Now we hash the password with the set_password method.
			# Once hashed, we can update the user object.
			user.set_password(user.password)
			user.save()

			# Now we sort out the UserProfile instance.
			# Since we need to set the user attribute ourselves, we set commit=False.
			# This delays saving the model until we're ready.
			profile = profile_form.save(commit=False)
			profile.user = user

			# Did the user provide a profile picture?
			# If so, we need to get it from the input form and put it in the UserProfile model.
			if 'picture' in request.FILES:
				profile.picture = request.FILES['picture']

			# Now we can save the profile instance.
			profile.save()

			# Update the variable to indicate that registration was successful.
			registered = True
		else:
			print(user_form.errors, profile_form.errors)
	else:

		# Not a HTTP POST, we render our view using two ModelForm instances.
		user_form = UserForm()
		profile_form = UserProfileForm()

	# Render the template depending on the context.
	return render(request, 'rango/register.html', context={'user_form': user_form, 'profile_form': profile_form, 'registered': registered})

def user_login(request):

	# If the request is a post, try to pull the relevant information.
	if request.method == 'POST':

		# Gether the username and password provided by the user; obtained from the login form.
		# Use get(<variable>) because [<variable>] will thrown an exception whilst the former returns None.
		username = request.POST.get('username')
		password = request.POST.get('password')

		# Use Djangos machinery to attempt to see if the username/password combination
		# is valid, a User object is returned if it is. Checks if an account exists.
		user = authenticate(username=username, password=password)

		# If we have the user object the details are correct.
		# If None, no user with matching credentials was found.
		if user:

			# Is the users account still activate? It could have been disabled.
			if user.is_active:

				# If the account is valid and active, we can log them in.
				# We'll send the user back to the homepage.
				login(request, user)
				return redirect(reverse('rango:index'))
			else:

				# An inactive account was used - no logging in.
				return HttpResponse('Your Rango account is disabled.')
		else:

			# Bad login details were provided - we cant log the user into an account.
			print(f'Invalid login details: {username}, {password}')
			return HttpResponse('Invalid details supplied.')

	else:

		# The request is not a HTTP POST, so display the login form; most likely a GET.
		# No context variables are passed, hence no dictionary.
		return render(request, 'rango/login.html')

@login_required
def user_logout(request):
	logout(request)
	return redirect(reverse('rango:index'))

# Python will execute the decorator before executing the code of your function / method.
# A decorator is still a function, thus must be imported.
@login_required
def restricted(request):
	return render(request, 'rango/restricted.html')







