from django.contrib.auth.models import User
from django.db import models


class ContactDetails(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=11, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
