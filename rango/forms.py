from django import forms
from rango.models import Category, Page

class CategoryForm(forms.ModelForm):
	name = forms.CharField(max_length=128, help_text='Please enter the category name.')
	views = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
	likes = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
	slug = forms.CharField(widget=forms.HiddenInput(), required=False)

	# An inline class to provide additional information to the form.
	class Meta:

		# Provide an association between ModelForm and the Model.
		model = Category

		# Specify the fields to include in the form.
		# Include (fields) or exclude (exclude) fields from the form.
		fields = ('name',)

class PageForm(forms.ModelForm):
	title = forms.CharField(max_length=Page.TITLE_MAX_LENGTH, help_text='Please enter the title of the page.')
	url = forms.URLField(max_length=Page.URL_MAX_LENGTH, help_text='Please enter the URL of the page.')
	views = forms.IntegerField(widget=forms.HiddenInput(), initial=0)

	# Additional information about the ModelForm.
	class Meta:

		# Provide an association between the form and the model.
		model = Page

		# What fields do we want to include in our form?
		# This was we dont need every field in the model.
		# Some fields may allow NULL, we don't want to include them.
		# Here, we are hiding the foreign key.
		# We can exclude the category field from the form.
		exclude = ('category',)

	# Called before a save occurs; prepend https to the start of the URL is does not exist.
	# Form data is obtained from ModelForm dictionary attribute.
	# Use .get to obtain the form value. If null (does not exist), get returns None opposed 
	# to a KeyError exception.
	def clean(self):
		cleaned_data = self.cleaned_data
		url = cleaned_data.get('url')

		# If the URL is not empty and doesnt start with http://, then prepend 'http://'
		if url and not url.startswith('http://'):
			url = f'http://{url}'
			cleaned_data['url'] = url

		# Apply the changes.
		return cleaned_data

