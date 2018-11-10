from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, View
from django.contrib.auth.decorators import login_required

from .models import JobEntry

def home(request):
	context = {
		'JobEntries' : JobEntry.objects.filter(author=request.user)
	}
	return render(request, 'main/user_entries.html', context)

class LandingView(View):

	def get(self, request):
		return render(request, 'main/landing.html')


class UserEntryListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
	model = JobEntry
	template_name = 'main/user_entries.html'
	context_object_name = 'JobEntries'
	ordering = ['-date_applied']

	def get_queryset(self):
		user = get_object_or_404(User, username=self.kwargs.get('username'))
		return JobEntry.objects.filter(author=user).order_by('-date_applied')
	
	
	def test_func(self):
		user = get_object_or_404(User, username=self.kwargs.get('username'))
		if self.request.user == user:
			return True
		else:
			return False
		

class EntryCreateView(LoginRequiredMixin, CreateView):
	model = JobEntry
	fields = ['position','company','city','state','salary', 'response']
	#success_url = 

	

	def form_valid(self, form):
		form.instance.author = self.request.user
		return super().form_valid(form)
	
	def get_success_url(self):
		return reverse('user-entries', args=[self.request.user.username])
	


class EntryUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
	model = JobEntry
	fields = ['position','company','city','state','salary', 'response']

	def get_success_url(self):
		return reverse('user-entries', args=[self.request.user.username])	

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

	def get_success_url(self):
		return reverse('user-entries', args=[self.request.user.username])
	def test_func(self):
		entry = self.get_object()
		if self.request.user == entry.author:
			return True
		return False

