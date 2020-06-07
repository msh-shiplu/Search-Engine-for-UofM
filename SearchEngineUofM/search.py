from django import forms


class SearchForm(forms.Form):
	search_box = forms.CharField(label='Search Box', max_length=100)

