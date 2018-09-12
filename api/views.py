import numpy as np
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_exempt
from rest_framework.authtoken.models import Token

from Data.forms import UserDataForm
from Data.models import UserData, Version, Profile
from StardewWeb.forms import SignUpForm
from api.forms import MessageForm
from api.models import Message


@csrf_exempt
def validate_token(request):
    """
    View to allow client to login at the startup of the desktop-app

    CLient should send POST request as:
    headers={"Authorization": f"Token {token}"}, data={'username': f'username'}
    """
    if request.method == 'POST':

        if 'username' in request.POST and 'HTTP_AUTHORIZATION' in request.META:
            try:
                username = request.POST['username']
                key = request.META['HTTP_AUTHORIZATION'].split(" ")[1]

                user = User.objects.get(username=username)
                token = Token.objects.get(key=key)

                if token.user == user:
                    return JsonResponse({"valid-token": True})
                else:
                    return JsonResponse({"valid-token": False})

            except:
                return JsonResponse({"valid-token": False})

        else:
            return JsonResponse({"valid-token": False, 'error': 'No auth token or username in POST request'})

    else:
        return render(request, '404.html')


@csrf_exempt
def api_create_account(request):
    if request.method == 'POST':

        form = SignUpForm(request.POST)

        if form.is_valid():

            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)

            login(request, user)
            token = Token.objects.get(user=user).key

            return JsonResponse({'success': True, 'token': token})

        else:
            return JsonResponse({'success': False, 'errors': form.errors.as_json()})

    else:
        return render(request, '404.html')


@csrf_exempt
def score_check(request):
    user_total_score = 0
    if request.method == 'POST':

        if 'username' in request.POST and 'HTTP_AUTHORIZATION' in request.META:
            try:
                username = request.POST['username']
                key = request.META['HTTP_AUTHORIZATION'].split(" ")[1]

                user = User.objects.get(username=username)
                token = Token.objects.get(key=key)

                if token.user == user:
                    user_scores = UserData.objects.filter(user=user)
                    user_total_score = sum([obj.score for obj in user_scores])

                else:
                    user_total_score = 0

            except:
                user_total_score = 0

    return JsonResponse({'score': user_total_score})


def version_control(request):
    version_control = [obj.as_dict() for obj in Version.objects.all()]
    return JsonResponse({"Version Control": version_control})


@csrf_exempt
def bug_report(request):
    if request.method == 'POST':

        # Gathering all info sent by the client
        try:
            key = request.META['HTTP_AUTHORIZATION'].split(" ")[1]
            username = request.POST['user']
            msg = request.POST['message']
            version = float(request.POST['version'])

        except:
            return JsonResponse({"success": False, "error": "Wrong formatting or missing information"})

        # Validating info
        try:

            user = User.objects.get(username__exact=username)
            version = Version.objects.get(version__exact=version)
            token = Token.objects.get(key=key)

        except:
            return JsonResponse({"success": False, "error": "User or version not found on database"})


        # Validanting form
        form = MessageForm({
            'message': msg,
            'user': user.id,
            'version': version.id,
        })

        # Checking authorization and form validity
        if form.is_valid() and token.user == user:

            message = Message(message=msg, user=user, version=version, read=False)
            message.save()

            return JsonResponse({"success": True})

        else:
            return JsonResponse({'success': False, 'error': 'Wrong formatting or missing information'})

    else:
        return render(request, '404.html')


@csrf_exempt
def data_upload(request):
    if request.method == 'POST':
        if request.FILES:

            try:
                username = request.POST['username']
                key = request.META['HTTP_AUTHORIZATION'].split(" ")[1]

                user = User.objects.get(username=username)
                token = Token.objects.get(key=key)

                if token.user == user:

                    form = UserDataForm(request.POST, request.FILES)

                    file = request.FILES['file']
                    version = request.POST['version']

                    version = Version.objects.get(version__exact=version)

                    if form.is_valid() and (file.name == 'training_data.npy'):  # and (file.size > 140000):

                        score = len(list(np.load(file)))
                        file = UserData(file=request.FILES['file'], user=user, score=score, processed=False,
                                        version=version)
                        file.save()

                        profile = Profile.objects.get(user=user)
                        profile.score += score
                        profile.save()

                        return JsonResponse({'success': True})

                    else:
                        return JsonResponse({
                            'success': False,
                            'valid form': form.is_valid(),
                            'file name': file.name,
                            'file size': file.size
                        })
                else:
                    return JsonResponse({"success": False, "error": "Not authorized"})


            except Exception as e:
                return JsonResponse({"success": False, "error": f"{e}"})

    else:
        return render(request, '404.html')

# def download(request):
#     file_path = 'Bot-Latest-Version/Globals.py'
#     if os.path.exists(file_path):
#         with open(file_path, 'rb') as fh:
#             response = HttpResponse(fh.read(), content_type="application/x-python")
#             response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
#             return response
