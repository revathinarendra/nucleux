from django.urls import path
from .views import   UserProfileEditView, VerifyEmailView
from accounts import views

urlpatterns = [
    
    #path('signup/', SignupView.as_view(), name='signup'),
    path('register/', views.register, name='register'),
    path('verify-email/<str:token>/', VerifyEmailView.as_view(), name='verify-email'),
    path('login/', views.login_view, name='login'),
    path('me/', views.currentUser, name='current_user'),
    path('password-reset/', views.password_reset_request, name='password-reset-request'),
    path('password-reset-confirm/<str:uidb64>/<str:token>/', views.password_reset_confirm, name='password-reset-confirm'), 
    path('edit-profile/', UserProfileEditView.as_view(), name='edit-profile'),
]
