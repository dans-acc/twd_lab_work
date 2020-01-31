from django.urls import path
from django.conf.urls import url # Necessary?
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

<slug:category_name_slug> is a parameter that is added to URL.
    Indicates to Django that we want to match a string which is a slug and assign it
    to variable category_name_slug.
    The variable names must match that foind in the function.
        You can match other parameters too, e.g. strings, integers etc.
'''

urlpatterns = [
	path('',views.index,name='index'),
	path('about/', views.about,name="about"),
	path('category/<slug:category_name_slug>/', views.show_category, name='show_category'),
	path('add_category/', views.add_category, name='add_category'),
	path('category/<slug:category_name_slug>/add_page/', views.add_page, name="add_page"),
]