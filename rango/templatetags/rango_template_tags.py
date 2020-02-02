from django import template
from rango.models import Category

register = template.Library()

'''
Create custom template tags that are included in the template
and allow them to request their data.

@register.inclusion_tag() director refers to another new template:
	"rango/categories.html".
	Used to render the list of categories you provide in the dictionary
	that is returned by the function.
	This can then be injected into the response of the view that initially
	called the template tag.

Returns a dictionary of all categories.
'''
@register.inclusion_tag('rango/categories.html')
def get_category_list(current_category=None):
	return {'categories': Category.objects.all(), 'current_category': current_category}