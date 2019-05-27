from django.db import models
""" This we are importing so that django doen not give any exception
    while we change the date time DateField"""
from django.utils.timezone import datetime

from django.contrib.auth.models import User
# Create your models here.

class Contact(models.Model):
    manager = models.ForeignKey(User , on_delete=models.CASCADE , default=None)
    name = models.CharField(max_length = 20)
    email = models.EmailField(max_length =100)
    phone = models.IntegerField()
    info = models.CharField(max_length = 30)
    gender = models.CharField(max_length = 50, choices= (
        ('male', 'Male'),
        ('female', 'Female')
    ) )

    # for image we need to install pillow so we do :: pip install pillow
    image = models.ImageField(upload_to = 'image/', blank = True)
    # Old - date_added = models.DateField(auto_now_add = True)
    """ NEW """
    date_added = models.DateTimeField(default = datetime.now )

    def __str__(self):
        return self.name

class Meta:
    ordering = ['-id']
