import json
import random
from datetime import datetime, timedelta

from django.db.models import Sum, Avg, Max
from django.shortcuts import render

from .models import UserData, Profile


def home_page(request):
    return render(request, 'home_page.html', context={})


def ranking(request):
    # Best Contributors table:
    # ----------------------------------------------------

    # Get best first 25 contributors from db
    best_friends = Profile.objects.order_by('-score')[:25]

    # Format data to json for frontend
    bffs = [{'user': profile.user, 'score': profile.score, 'position': i + 1} for i, profile in enumerate(best_friends)]

    # Graph data:
    # ----------------------------------------------------

    # Creating list of days of this week
    days_this_week = []
    today = datetime.today().date()
    for i in range(8):
        date = (today + timedelta(days=-i))
        days_this_week.append(str(date))

    # Creating list of scores from this week
    score_this_week = []
    for i in range(8):
        score = sum([obj.score for obj in
                     UserData.objects.filter(uploaded_at__date=datetime.today().date() - timedelta(days=i))])
        score_this_week.append(score)

    # Zipping scores and dates into one dict
    data = dict(zip(days_this_week, score_this_week))

    # Progress Bar data:
    # ----------------------------------------------------
    score_sum = Profile.objects.aggregate(Sum('score'))['score__sum']

    # Percent of individual help
    total_time_played = round(score_sum / 3600, 2)
    if request.user.is_authenticated and score_sum > 0:
        help_percent = round(100 * (Profile.objects.get(user=request.user).score) / score_sum, 1)
    else:
        help_percent = 0

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

    # Number of users:
    # ----------------------------------------------------
    n_users = Profile.objects.all().count()

    # Average number of frames per user
    # ----------------------------------------------------
    avg_user_score = round(Profile.objects.aggregate(Avg('score'))['score__avg'])

    # Average number of sessions per user
    # ----------------------------------------------------
    avg_session_score = UserData.objects.aggregate(Avg('score'))['score__avg']

    avg_session_score = round(avg_session_score) if avg_session_score is not None else 0
    avg_session_time = round(avg_session_score / 60, 2) if avg_session_score is not None else 0

    # Top 3 users
    # ----------------------------------------------------
    top_3_score_sum = Profile.objects.order_by('-score')[:3].aggregate(Sum('score'))['score__sum']
    if top_3_score_sum is not None and score_sum > 0:
        top_3_score_percent = round(100 * top_3_score_sum / score_sum, 2)
    else:
        top_3_score_percent = 0

    # Longest fishing session
    # ----------------------------------------------------
    max_score = UserData.objects.aggregate(Max('score'))['score__max']
    max_score_users = UserData.objects.filter(score=max_score)

    if max_score_users is not None and max_score is not None:
        rand_user = random.randint(0, len(max_score_users) - 1)

        max_score_user = [user for user in max_score_users][rand_user]
        time = round(max_score/60, 1)
    else:
        max_score = 0
        max_score_user = 'admin'
        time = 0

    longest_session_dict = {'max_score': max_score, 'user': max_score_user, 'time': time}

    return render(request, 'dashboard.html', context={

        'bffs_dict': bffs,
        'data': json.dumps(data),
        'score_sum': score_sum,
        'total_time_played': total_time_played,
        'user_data': user_data,
        'help_percent': help_percent,
        'n_users': n_users,
        'avg_user_score': avg_user_score,
        'avg_session_score': avg_session_score,
        'avg_session_time': avg_session_time,
        'top_3_score_percent': top_3_score_percent,
        'longest_session': longest_session_dict,
    })
