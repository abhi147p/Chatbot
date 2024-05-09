
# Create your models here.
from django.db import models
from django.contrib.auth.models import User
import datetime
from django.utils import timezone

class OTP(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    time_stamp = models.DateTimeField(auto_now=True)
    otp = models.IntegerField()

    def is_valid(self):
        return (datetime.datetime.now() - self.time_stamp).seconds < 300  # valid for 5 minutes

class History(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='history')
    description = models.CharField(max_length=255)
    timestamp = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f'{self.user.username} - {self.description} at {self.timestamp}'

    class Meta:
        ordering = ['-timestamp']