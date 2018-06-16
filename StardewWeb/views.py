from django.http import JsonResponse
from Data.models import UserData, Version
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from .forms import SignUpForm
from django.views import generic
import os, datetime

def home_page(request):
    """
    View function for the home page
    """

    return render(request, 'home_page.html', context={})

@login_required
def score_data(request):
    try:
        user_scores = UserData.objects.filter(user=request.user)
        user_total_score = sum([obj.score for obj in user_scores])
    except:
        user_total_score = 0
    return JsonResponse({'score': user_total_score})


def version_control(request):
    version_control = [obj.as_dict() for obj in Version.objects.all()]
    return JsonResponse({"Version Control": version_control})


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('home page')
    else:
        form = SignUpForm()
    return render(request, 'registration/signup.html', {'form': form})
