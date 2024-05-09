from django.shortcuts import render, redirect
from .forms import SignUpForm, OTPForm
from django.contrib.auth import authenticate, login
from .models import OTP, History
from django.contrib.auth.models import User
from django.core.mail import send_mail
import random
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.core.mail import send_mail, EmailMessage
from django.template.loader import render_to_string

def get_history(user):
    from django.utils import timezone
    from datetime import timedelta

    today = timezone.now()
    yesterday = today - timedelta(days=1)
    last_7_days = today - timedelta(days=7)
    last_30_days = today - timedelta(days=30)

    history = {
        'today': History.objects.filter(user=user, timestamp__date=today.date()),
        'yesterday': History.objects.filter(user=user, timestamp__date=yesterday.date()),
        'last_7_days': History.objects.filter(user=user, timestamp__gte=last_7_days.date()),
        'last_30_days': History.objects.filter(user=user, timestamp__gte=last_30_days.date()),
    }
    return history

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False  # User will be activated after OTP verification
            user.save()
            otp = random.randint(1000, 9999)
            OTP.objects.create(user=user, otp=otp)
            send_otp_via_email(user.email, otp)
            return redirect('otp_verification', user.id)
    else:
        form = SignUpForm()
    return render(request, 'chatbot_app/signup.html', {'form': form})

def otp_verification(request, user_id):
    user = User.objects.get(id=user_id)
    if request.method == 'POST':
        form = OTPForm(request.POST)
        if form.is_valid():
            user_otp = form.cleaned_data['otp']
            otp_instance = OTP.objects.filter(user=user).order_by('-time_stamp').first()
            if otp_instance and otp_instance.is_valid() and otp_instance.otp == user_otp:
                user.is_active = True
                user.save()
                login(request, user)
                return redirect('home')  # Assuming 'home' is the route name of your main page after login
            else:
                return render(request, 'chatbot_app/otp_verification.html', {'form': form, 'error': 'Invalid OTP', 'user_id': user_id})
    else:
        form = OTPForm()
    return render(request, 'chatbot_app/otp_verification.html', {'form': form, 'user_id': user_id})

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')  # Redirect to a success page
        else:
            return render(request, 'chatbot_app/login.html', {'error': 'Invalid username or password'})
    else:
        return render(request, 'chatbot_app/login.html')

@require_http_methods(["DELETE"])
def delete_history(request, history_id):
    try:
        history = History.objects.get(id=history_id, user=request.user)
        history.delete()
        return JsonResponse({"success": True})
    except History.DoesNotExist:
        return JsonResponse({"success": False})

def send_email(subject, message, from_mail, to_list, fail_silently=False):
    send_mail(
        subject,
        message,
        from_mail,
        to_list,
        fail_silently
    )


def send_otp_via_email(mail_id, otp, user):
    subject = 'Your OTP for Registration - CHATBOT'
    message = render_to_string('accounts/otp_email_template.html', {'user': user, 'otp_code': otp})
    from_email = 'ChatBot.acc.in'
    recipient_list = [mail_id]

    email_message = EmailMessage(subject, message, from_email, recipient_list)
    email_message.content_subtype = 'html'
    email_message.send()


# def send_otp_via_email(email, otp):
#     send_mail(
#         'Your OTP',
#         f'Your OTP is {otp}',
#         'from@example.com',
#         [email],
#         fail_silently=False,
#     )

