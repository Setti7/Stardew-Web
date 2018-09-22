from django.contrib.auth import views as auth_views
from django.urls import path

from Account import views

urlpatterns = [

    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('create/', views.signup, name='create account'),

    path('account-reset', auth_views.password_reset,
         {'html_email_template_name': 'registration/password_reset_email.html'}, name='password_reset'),
    path('account-reset/done', auth_views.password_reset_done, name='password_reset_done'),
    path('password-reset/token/<uidb64>/<token>', auth_views.password_reset_confirm, name='password_reset_confirm'),
    path('password-reset/done', auth_views.password_reset_complete, name='password_reset_complete'),

]
