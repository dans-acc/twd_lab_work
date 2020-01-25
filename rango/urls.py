from django.urls import path
from rango import views

app_name = 'rango'

'''
We assume that the host portion has already been stripped out.
	The host portion denotes the host address or domain name that maps
	to the web server, e.g:
		http://127.0.0.1:8000; or
		http://www.tangowithdjango.com

	Means that we only need to handle the remainder of the URL string.

The parameter for the path function is the string to match.
	Empty string means that a match will be found when nothing is there.
The second parameter for path() is the view that's to be called.
	view.index() will be called.
The third parameter, name, is an _optional_ parameter.
	provides a convenient way to reference the view;
	can employ reverse url matching:
		we can reference it by name rather than url.
'''

urlpatterns = [
	path('',views.index,name='index'),
]