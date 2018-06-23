from django.http import JsonResponse, HttpResponse
import numpy as np
from Data.models import UserData, Version
from Data.forms import UserDataForm
from StardewWeb.forms import SignUpForm
import os, datetime
from django.contrib.auth import login, authenticate
from django.views.decorators.csrf import ensure_csrf_cookie


@ensure_csrf_cookie
def api_login(request):
    if request.method == 'POST':

        try:
            username = request.POST['username']
            password = request.POST['password']

            user = authenticate(username=username, password=password)

            login(request, user)

            return JsonResponse({'success': True})

        except Exception as e:
            return JsonResponse({'success': False})
    else:
        return HttpResponse('You should not be here, this is only for the api!<br><br><strong>BEGONE THOT!</strong>')


@ensure_csrf_cookie
def api_create_account(request):
    if request.method == 'POST':

        form = SignUpForm(request.POST)

        if form.is_valid():

            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)

            login(request, user)

            return JsonResponse({'success': True})

        else:
            return JsonResponse({'success': False})

    else:
        return HttpResponse('You should not be here, this is only for the api!<br><br><strong>BEGONE THOT!</strong>')


def score(request):
    try:
        user_scores = UserData.objects.filter(user=request.user)
        user_total_score = sum([obj.score for obj in user_scores])

    except:
        user_total_score = 0

    return JsonResponse({'score': user_total_score})


def version_control(request):
    version_control = [obj.as_dict() for obj in Version.objects.all()]
    return JsonResponse({"Version Control": version_control})


def bug_report(request):
    if request.method == 'POST':
        try:
            msg = request.POST['msg']
            user = request.POST['user']
            contact = request.POST['contact']

        except:
            return JsonResponse({'success': False, 'error': 'data sent in wrong format or missing something'})

        if os.path.isfile('media\\messages\\{}.txt'.format(user)):
            with open('media\\messages\\{}.txt'.format(user), 'a') as f:
                date = datetime.datetime.now()
                f.write(
                    "{:%Y-%m-%d %H:%M:%S}\n\n{}\n\nContact: {}\n---------------------------------\n".format(
                        date, msg, contact
                    ))

        else:
            with open('media\\messages\\{}.txt'.format(user), 'w') as f:
                date = datetime.datetime.now()
                f.write(
                    "{:%Y-%m-%d %H:%M:%S}\n\n{}\n\nContact: {}\n---------------------------------\n".format(
                        date, msg, contact
                    ))

        return JsonResponse({"success": True})

    else:
        return HttpResponse('You should not be here, this is only for the api!<br><br><strong>BEGONE THOT!</strong>')


def data_upload(request):
    if request.method == 'POST':
        if request.FILES:
            form = UserDataForm(request.POST, request.FILES)

            file = request.FILES['file']

            if form.is_valid() and (file.name == 'training_data.npy') and (file.size > 140000):

                score = len(list(np.load(file)))
                file = UserData(file=request.FILES['file'], user=request.user, score=score)
                file.save()

                return JsonResponse({'success': True}) # status 200

            else:
                return JsonResponse({
                    'success': False,
                    'valid form': form.is_valid(),
                    'file name': file.name,
                    'file size': file.size
                }) # status 201

    else:
        return HttpResponse('You should not be here, this is only for the api!<br><br><strong>BEGONE THOT!</strong>')
