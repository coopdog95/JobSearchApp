from django.shortcuts import render
from .models import JobEntry

def home(request):
	context = { 
	'JobEntrys' : JobEntry.objects.all() 
	}
	return render(request, 'main/table.html', context)
