from django.db import models

# Create your models here.


class Address(models.Model):
    type = models.CharField(max_length=128, default='')
    project = models.ForeignKey('Project', blank=True, null=True)

    name = models.CharField(max_length=128, blank=True)
    company = models.CharField(max_length=128, blank=True)
    street1 = models.CharField(max_length=128, blank=True)    
    street2 = models.CharField(max_length=128, blank=True)
    city = models.CharField(max_length=128, blank=True)    
    province = models.CharField(max_length=128, blank=True)
    postal_code = models.CharField(max_length=128, blank=True)
    country = models.CharField(max_length=128, blank=True)
    phone = models.CharField(max_length=128, blank=True)
    email = models.EmailField(max_length=128, blank=True)

    def __unicode__(self):
        return '{self.type}: {self.name} [{self.company}]'.format(
            self=self,)


class Project(models.Model):
    name = models.CharField(max_length=528)
    hourly_rate = models.DecimalField(max_digits=12, decimal_places=2)
    
    default_ship_address = models.ForeignKey(Address, related_name="default_ship_projects")
    company = models.ForeignKey(Address, related_name="related_projects")


class ProjectHours(models.Model):
    project = models.ForeignKey(Project)

    start_time = models.DateTimeField()
    end_time = models.DateTimeField(blank=True, null=True)

    minutes = models.DecimalField(max_digits=12, decimal_places=4, default=0)
    comment = models.TextField(blank=True)
    paid = models.BooleanField(default=False, blank=True)

    def __unicode__(self):
        return '{self.start_time} - {self.end_time}'.format(self=self)

    def save(self, *args, **kwargs):
        if self.start_time and self.end_time:
            self.minutes = (self.end_time - self.start_time).seconds / 60
        super(ProjectHours, self).save(*args, **kwargs)


class Invoice(models.Model):
    project = models.ForeignKey(Project)
    paid = models.BooleanField(default=False, blank=True)
    amount = models.DecimalField(decimal_places=2, max_digits=12, default=0)
    hours = models.ManyToManyField(ProjectHours, blank=True, null=True)

    comment = models.TextField(blank=True)

    PAYMENT_TYPE_CHOICES = [
        ('Cash', 'Cash'),
        ('Check', 'Check'),
        ('PayPal', 'PayPal'),
        ('Credit Card', 'Credit Card'),
        ('Bank Transfer', 'Bank Transfer'),
    ]
    payment_type = models.CharField(max_length=256, choices=PAYMENT_TYPE_CHOICES)

    billing_address = models.ForeignKey(Address, blank=True, null=True, related_name="+")
    shipping_address = models.ForeignKey(Address, blank=True, null=True, related_name="+")

    def calculate_amount(self):
        return self.hours.aggregate(s=models.Sum('minutes')).get('s', 0)


