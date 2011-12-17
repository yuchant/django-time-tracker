from django.db import models

# Create your models here.

class Project(models.Model):
	name = models.CharField(max_length=528)
	hourly_rate = models.DecimalField(max_digits=12, decimal_places=2)


class ProjectHours(models.Model):
	project = models.ForeignKey(Project)

	start_time = models.DateTimeField()
	end_time = models.DateTimeField(blank=True, null=True)

	comment = models.TextField(blank=True)

	def __unicode__(self):
		return '{self.start_time} - {self.end_time}'.format(self=self)