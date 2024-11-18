from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('otp_verification/<int:user_id>/', views.otp_verification, name='otp_verification'),
    path('login/', views.login_view, name='login'),
    path('delete-history/<int:history_id>/', views.delete_history, name='delete_history'),
    path('home/', views.home, name='home'),
    path('logout/', views.logoutPage, name='logout'),
    # Add other URLs as needed
]
