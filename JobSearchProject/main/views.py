from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, View
from django.contrib.auth.decorators import login_required
from rest_framework import filters
from django.db.models import Q
import re, operator
from functools import reduce

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
	#ordering = ['-date_applied']
	filter_backends = (filters.SearchFilter)
	#search_fields = ('position','company','city')

	

	def get_queryset(self):
		user = get_object_or_404(User, username=self.kwargs.get('username'))
		ordering = self.request.GET.get('ordering', 'date_applied')
		order = self.request.GET.get('order', 'desc')
		
		if order == 'desc':
			ordering = "-" + ordering

		query = self.request.GET.get('search')
		result = super(UserEntryListView, self).get_queryset()
		if query:
			query_list = query.split()
			result = result.filter(
				reduce(operator.and_,
					(Q(position__icontains=q) for q in query_list)) |
				reduce(operator.and_,
					(Q(company__icontains=q) for q in query_list)) |
				reduce(operator.and_,
					(Q(city__icontains=q) for q in query_list)) |
				reduce(operator.and_,
					(Q(state__icontains=q) for q in query_list))
				)
			return result.filter(author=user)
	
		return JobEntry.objects.filter(author=user).order_by(ordering)
	
	def get_context_data(self, *args, **kwargs):
		context = super(UserEntryListView, self).get_context_data(**kwargs)
		context['sortby'] = self.request.GET.get('ordering', 'date_applied')
		context['order'] = self.request.GET.get('order', 'desc')
		if context['order'] == 'desc':
			context['sortby'] = "-"+context['sortby']
		return context
	
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

