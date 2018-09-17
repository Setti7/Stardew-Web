from django.shortcuts import render, redirect, HttpResponseRedirect
from django.http import JsonResponse, Http404
from django.contrib.auth.decorators import login_required
from django.db.models import Sum, Count
from .forms import UserDataForm
from itertools import groupby
from .models import UserData, Profile
import numpy as np
import json, os
from datetime import datetime, timedelta, date
from StardewWeb.settings import MEDIA_ROOT


def home_page(request):
    return render(request, 'home_page.html', context={})

# TODO: fazer o post request de deletar dados como javascript, pra não ter que recarregar página
def ranking(request):

    # Best Contributors table:
    # ----------------------------------------------------

    # Get best first 18 contributors from db
    best_friends = Profile.objects.order_by('-score')[:18]

    # Format data to json for frontend
    bffs = [{'user': profile.user, 'score': profile.score, 'position': i + 1} for i, profile in enumerate(best_friends)]

    # Graph data:
    # ----------------------------------------------------
    last_week = datetime.now() - timedelta(days=7)

    # Creates a list of dicts of all users' scores, with upload date. Eg: [{'date': 2018-1-22, 'score':122}, {'date': 2018-1-22, 'score':1212}, {'date': 2018-1-23, 'score':245}]
    lst = [{
            "date": str(obj.uploaded_at.date()),
            "score": obj.score
            }
            for obj in UserData.objects.filter(uploaded_at__gt=last_week).order_by('uploaded_at')
        ]

    # Group the scores from the list of dicts, with respect to the date.
    data = {}
    for key, value in groupby(lst, key=lambda x: x['date']):
        scores = [dict["score"] for dict in list(value)]
        data[key] = sum(scores)


    # Progress Bar data:
    # ----------------------------------------------------
    pro_data = UserData.objects.aggregate(Sum('score'))['score__sum']


    # Data Submitted:
    # ----------------------------------------------------
    if request.user.is_authenticated:
        uploads = UserData.objects.filter(user=request.user).order_by('-uploaded_at')

        user_data = []
        for upload in uploads:
            date = upload.uploaded_at.strftime('%Y-%m-%d %H:%M:%S')
            user_data.append({"score": upload.score, "id": upload.id, "uploaded_at": date})

    else:
        user_data = {}

    return render(request, 'dashboard.html', context={

        'bffs_dict': bffs,
        'data': json.dumps(data),
        'score_sum': pro_data,
        'user_data': user_data
    })
