from django.shortcuts import render
import os
from django.conf import settings
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from difflib import SequenceMatcher

# Create your views here.
def home(request):
	import requests
	import json
	# api_request = requests.get('https://min-api.cryptocompare.com/data/v2/news/?lang=EN')
	# api_text = json.loads(movies_tables.json)

	with  open(os.path.join(settings.BASE_DIR,'crypto\\movies_tables.json')) as f:
		api_text = json.load(f)

	page = request.GET.get('page', 1)
	search = request.GET.get('search', None)

	idx_list = []
	if search:
		for idx, item in enumerate(api_text):
			# print(item['movie_name'], idx)
			# print(item['movie_name'], round(SequenceMatcher(None,item['movie_name'].lower(), search.lower()).ratio(),2))
			if round(SequenceMatcher(None,item['movie_name'].lower(), search.lower()).ratio(),2)>0.55:
				idx_list.append(idx)
				# print(item['movie_name'], round(SequenceMatcher(None,item['movie_name'].lower(), search.lower()).ratio(),2))
			# print(search, "SequenceMatcher")

		# print(idx_list, idx)
		api_text = [api_text[id1] for id1  in idx_list]
		# print(api_text)
	# print("PAGE", page)
	if search:
		paginator = Paginator(api_text, len(idx_list))
	else:
		paginator = Paginator(api_text, 12)
	try:
		data_text = paginator.page(page)
	except PageNotAnInteger:
		data_text= paginator.page(1)
	except EmptyPage:
		data_text = paginator.page(paginator.num_pages)
	print( Paginator(api_text, 12).num_pages)
	return render(request, 'home.html', {'api':data_text})
