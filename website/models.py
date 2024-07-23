from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.db import models


class User(AbstractUser):
    pass

class Category(models.Model):
    type = models.CharField(max_length=100)
    
    def __str__(self):
        return self.type

class Patient(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    service = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="type_of")
    email = models.EmailField()
    phone_number = models.CharField(max_length=16)
    details = models.TextField(max_length=3000, null=True, blank=True)
    appt_date = models.DateTimeField()
    date_added = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True, blank=True)
    is_done = models.BooleanField(default=False, blank=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True, related_name="booker")
    
    def __str__(self):
        return f"{self.first_name} {self.last_name} for {self.service} - {self.phone_number} {self.email} - {self.date_added} booked by {self.user}"