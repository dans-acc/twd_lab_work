"""twd_lab_work URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.urls import include

from rango import views

'''
    Maps the basic URL to the index view; maps anything begining with rango to be handled by rango.
    The added mapping looks for URL strings beginning with rango/.
        When the match is made, the remainder of the URL string is then passed onto and handled by rango.urls
        through the use of include().
'''
urlpatterns = [
    path('', views.index, name="index"),
    path('rango/', include('rango.urls')),
    path('admin/', admin.site.urls),
]
