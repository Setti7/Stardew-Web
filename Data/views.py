from django.shortcuts import render

# Create your views here.

def ranking(request):
    return render(request, 'dashboard.html', context={})