from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from .forms import SignUpForm


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

def error_404(request):
    return render(request, '404.html')

def error_500(request):
    return render(request, '500.html')

def error_400(request):
    return render(request, '400.html')

def error_403(request):
    return render(request, '403.html')

