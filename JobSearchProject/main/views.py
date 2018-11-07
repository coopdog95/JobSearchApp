from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from .models import JobEntry


def home(request):
	context = { 
	'JobEntries' : JobEntry.objects.filter(user=request.user)
	}
	return render(request, 'main/user_entries.html', context)
	#this return should bring user to landing page instead of entries

class LandingView():
	template_name = 'landing.html'

class EntryListView(ListView):
	model = JobEntry
	template_name = 'main/table.html'
	context_object_name = 'JobEntries'
	ordering = ['-date_applied']

class UserEntryListView(ListView):
	model = JobEntry
	template_name = 'main/user_entries.html'
	context_object_name = 'JobEntries'
	ordering = ['-date_applied']

	def get_queryset(self):
		user = get_object_or_404(User, username=self.kwargs.get('username'))
		return JobEntry.objects.filter(author=user).order_by('-date_applied')



class EntryCreateView(LoginRequiredMixin, CreateView):
	model = JobEntry
	fields = ['position','company','city','state','salary']
	success_url = '/'
	

	def form_valid(self, form):
		form.instance.author = self.request.user
		return super().form_valid(form)




class EntryUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
	model = JobEntry
	fields = ['position','company','city','state','salary']
	success_url = '/'
	

	def form_valid(self, form):
		form.instance.author = self.request.user
		return super().form_valid(form)

	def test_func(self):
		entry = self.get_object()
		if self.request.user == entry.author:
			return True
		return False




class EntryDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
	model = JobEntry
	success_url = '/'

	def test_func(self):
		entry = self.get_object()
		if self.request.user == entry.author:
			return True
		return False

