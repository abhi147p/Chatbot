
# Create your models here.
from django.db import models
from django.contrib.auth.models import User
import datetime
from django.utils import timezone

class ChatMessage(models.Model):
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    is_user = models.BooleanField(default=True)  # True if message from user, False if from bot

    def __str__(self):
        return self.text

class OTP(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    time_stamp = models.DateTimeField(auto_now=True)
    otp = models.IntegerField()

    def is_valid(self):
        # OTP is valid for 5 minutes
        return (datetime.datetime.now(datetime.timezone.utc) - self.time_stamp).total_seconds() < 300

    def is_expired(self):
        # OTP is expired after 5 minutes
        return (datetime.datetime.now(datetime.timezone.utc) - self.time_stamp).total_seconds() > 300
    
class History(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='history')
    description = models.CharField(max_length=255)
    timestamp = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f'{self.user.username} - {self.description} at {self.timestamp}'

    class Meta:
        ordering = ['-timestamp']