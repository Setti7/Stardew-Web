from django.shortcuts import render
from django.http import JsonResponse
from Data.models import UserData
from datetime import datetime, timedelta
from itertools import groupby
import json

def home_page(request):
    """
    View function for the home page
    """

    return render(request, 'home_page.html', context={})


def score_data(request):
    score = UserData.objects.get(user=request.user).score
    return JsonResponse({'score': score})
