from django.contrib.auth import login, authenticate
# Avoid shadowing the login() and logout() views below.
from django.contrib.auth import (
    login as auth_login,
)
from django.contrib.auth.views import LoginView
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect

from .forms import SignUpForm

def login_cancelled(request):
    return redirect('home page')

#
# def signup(request):
#     if request.method == 'POST':
#         form = SignUpForm(request.POST)
#         if form.is_valid():
#             form.save()
#             username = form.cleaned_data.get('username')
#             raw_password = form.cleaned_data.get('password1')
#             user = authenticate(username=username, password=raw_password)
#             login(request, user)
#             return redirect('home page')
#     else:
#         form = SignUpForm()
#     return render(request, 'registration/signup.html', {'form': form})
#
#
# class CustomLoginView(LoginView):
#     """
#     Display the login form and handle the login action.
#     """
#
#     def form_valid(self, form):
#         """Security check complete. Log the user in."""
#         auth_login(self.request, form.get_user())
#
#         # If user does NOT check remember-me box, set session expiry to 0
#         if not self.request.POST.get('remember_me', None):
#             self.request.session.set_expiry(0)
#
#         return HttpResponseRedirect(self.get_success_url())
