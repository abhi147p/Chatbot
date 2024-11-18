from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True, help_text='Required. Inform a valid email address.')

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password1', 'password2']

class OTPForm(forms.Form):
    otp = forms.IntegerField(help_text='Enter OTP')
    
class MessageForm(forms.Form):
    message = forms.CharField(label='Your message', max_length=1000)