from django.shortcuts import render
from django.http import HttpResponseRedirect


from .search import SearchForm
from . import invertedindex

def get_search(request):
	form = SearchForm()
	return render(request, 'search.html', {'form': form})


def get_search_result(request):
	query = request.GET.get('search_box')
	result = invertedindex.get_query_result(query)
	context = {'query':query, 'result':result, 'size': len(result)}
	return render(request, 'search-result.html', context)
