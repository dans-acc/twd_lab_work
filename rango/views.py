from django.shortcuts import render
from django.http import HttpResponse

'''
The functions are called from the urls.py inside the rango app.
'''

# Create your views here.
def index(request):
	
	'''
	Dictionary to pass to the template engine as its context.
	boldmessage matches to {{boldmessage}} in template.
	'''
	context_dict = {'boldmessage':'Crunchy, creamy, cookie, candy, cupcake!'}

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