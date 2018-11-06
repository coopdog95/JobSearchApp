from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class JobEntry(models.Model):
	author = models.ForeignKey(User, on_delete=models.CASCADE)
	position = models.CharField(max_length=100)
	company = models.CharField(max_length=100)
	date_applied = models.DateTimeField(default=timezone.now)
	city = models.CharField(max_length=100, null=True)
	state = models.CharField(max_length=2, null=True)
	salary = models.IntegerField(default=0)
	response = models.CharField(max_length=1,null=False, default='N')

	def __str__(self):
		return (self.position+" "+self.company+" "+self.city+" "+self.state+" "+str(self.salary)+" "+self.response)
				