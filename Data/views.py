from django.shortcuts import render, redirect, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from .forms import UserDataForm
from itertools import groupby
from .models import UserData
import numpy as np
import json, os
from datetime import datetime, timedelta, date
from StardewWeb.settings import MEDIA_ROOT


def ranking(request):

    # File upload:
    # ----------------------------------------------------
    submitted = ''
    if request.method == 'POST':
        form = UserDataForm(request.POST, request.FILES)

        file = request.FILES['file']
        submitted = 'False'

        if form.is_valid() and (file.name == 'training_data.npy') and (file.size > 100):

            score = len(list(np.load(file)))

            # UserData.objects.filter(user=request.user).delete()
            # folder = os.path.join(MEDIA_ROOT, "userdata/{0}".format(request.user))
            #
            # Deleting old files on the user folder
            # try:
            #     for things in os.listdir(folder):
            #         things_path = os.path.join(folder, things)
            #         if os.path.isfile(things_path):
            #             os.unlink(things_path)
            # except Exception as e:
            #     print(e)

            file = UserData(file=request.FILES['file'], user=request.user, score=score)

            file.save()
            submitted = 'True'

            redirect('ranking/')

        else:

            if 'PROGRAM' in request.POST:
                return HttpResponseRedirect('ranking/', status=201)
    else:

        form = UserDataForm()

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
    lst = [{"date": str(obj.uploaded_at.date()), "score": obj.score} for obj in UserData.objects
        .filter(uploaded_at__gt=last_week)
        .order_by('uploaded_at')]

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
            filename = os.path.split(str(upload.file))[1]
            filename = os.path.splitext(filename)[0]
            date = upload.uploaded_at.strftime('%Y-%m-%d %H:%M:%S')

            user_data.append({"score": upload.score, "id": filename, "uploaded_at": date})
    else:
        user_data = {}

    return render(request, 'dashboard.html', context={
        'form': form,
        'submitted': submitted,
        'bffs_dict': bffs,
        'data': json.dumps(data),
        'score_sum': pro_data,
        'user_data': user_data
    })
