from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from django.shortcuts import redirect, render
from .choices import *


class JobEntry(models.Model):
	author = models.ForeignKey(User, on_delete=models.CASCADE)
	position = models.CharField(max_length=100)
	company = models.CharField(max_length=100)
	date_applied = models.DateTimeField(default=timezone.now)
	city = models.CharField(max_length=100, null=True)
	state = models.CharField(max_length=2, null=True)
	salary = models.IntegerField(default=0)
	response = models.IntegerField(choices=RESPONSE_CHOICES, default=1)

	def __str__(self):
		return (self.position+" "+self.company+" "+self.city+" "+self.state+" "+str(self.salary))
	