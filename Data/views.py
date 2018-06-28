from django.shortcuts import render, redirect, HttpResponseRedirect
from django.http import JsonResponse, Http404
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from .forms import UserDataForm
from itertools import groupby
from .models import UserData
import numpy as np
import json, os
from datetime import datetime, timedelta, date
from StardewWeb.settings import MEDIA_ROOT


def home_page(request):
    return render(request, 'home_page.html', context={})

# TODO: fazer o post request de deletar dados como javascript, pra não ter que recarregar página
def ranking(request):

    # Delete button:
    # ----------------------------------------------------
    if request.method == 'POST':
        item_id = request.POST.get('data_id')
        item = UserData.objects.get(id=item_id)

        # There must be a simple verifcation so check if the user who sent the request is the owner of the data
        if request.user == item.user:
            file = os.path.join('media', str(item.file))
            if os.path.isfile(file):
                os.unlink(file)
                item.delete()

        return HttpResponseRedirect('/ranking')

    # Best Contributors table:
    # ----------------------------------------------------
    # Get all users from database
    list_of_users=[]
    for obj in UserData.objects.all():
        list_of_users.append(tuple((obj.user.username, obj.score)))

    # Make a dict of every user, with its score sum
    every_user = {}
    for key, value in list_of_users:
        every_user[key] = every_user.get(key, 0) + value

    sorted_users = sorted(every_user, key=every_user.get, reverse=True)[:18]

    # Separate the dict into a list of dicts, so django template engine can work
    bffs = []
    for user in sorted_users:
        bffs.append({"user": user , "score": every_user[user]})

        # Stop loop when the top 18 users are found
        if len(bffs) >= 18:
            break

    for n, item in enumerate(bffs):
        item.update({"position": n+1})


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
