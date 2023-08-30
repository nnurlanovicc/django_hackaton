from django.urls import path
from .views import RegistrationView,ActivationView,loginView,LogoutView,UserListView,ChangePasswordView,ForgotPasswordView,ForgotPasswordCompleteView

urlpatterns = [
    path('register/', RegistrationView.as_view()),
    path('activate/', ActivationView.as_view()),
    path('login/', loginView.as_view()),
    path('logout/', LogoutView.as_view()),
    path('users/', UserListView.as_view()),
    path('change_pass/', ChangePasswordView.as_view()),
    path('forgot_pass/', ForgotPasswordView.as_view()),
    path('forgot_pass_comp/', ForgotPasswordCompleteView.as_view()),

]