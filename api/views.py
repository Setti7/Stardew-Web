import numpy as np
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from django.views.decorators.csrf import ensure_csrf_cookie

from Data.forms import UserDataForm
from Data.models import UserData, Version
from StardewWeb.forms import SignUpForm
from api.forms import MessageForm
from api.models import Message


@ensure_csrf_cookie
def api_login(request):
    if request.method == 'POST':

        try:
            username = request.POST['username']
            password = request.POST['password']

            user = authenticate(username=username, password=password)

            login(request, user)

            return JsonResponse({'success': True})

        except:
            return JsonResponse({'success': False})

    else:
        return render(request, '404.html')


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
        return render(request, '404.html')


@login_required
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


@login_required
def bug_report(request):
    if request.method == 'POST':

        username = request.POST['user']
        msg = request.POST['message']
        contact = request.POST['contact']
        version = float(request.POST['version'])
        print(version)

        if contact == 'False':
            contact = None

        user = User.objects.get(username__exact=username)
        version = get_object_or_404(Version, version=version)

        form = MessageForm({
            'csrfmiddlewaretoken': request.POST['csrfmiddlewaretoken'],
            'message': msg,
            'user': user.id,
            'contact': contact,
            'version': version.id,
        })

        if form.is_valid() and request.user == user:

            message = Message(message=msg, user=user, contact=contact, version=version, read=False)
            message.save()

            return JsonResponse({"success": True})

        else:
            return JsonResponse({'success': False, 'error': 'data sent in wrong format or missing something'})

    else:
        return render(request, '404.html')


@login_required
def data_upload(request):
    if request.method == 'POST':
        if request.FILES:
            form = UserDataForm(request.POST, request.FILES)

            file = request.FILES['file']
            version = request.POST['version']

            version = Version.objects.get(version__exact=version)

            if form.is_valid() and (file.name == 'training_data.npy'):  # and (file.size > 140000):

                score = len(list(np.load(file)))
                file = UserData(file=request.FILES['file'], user=request.user, score=score, processed=False,
                                version=version)
                file.save()

                return JsonResponse({'success': True})

            else:
                return JsonResponse({
                    'success': False,
                    'valid form': form.is_valid(),
                    'file name': file.name,
                    'file size': file.size
                })

    else:
        return render(request, '404.html')

# def download(request):
#     file_path = 'Bot-Latest-Version/Globals.py'
#     if os.path.exists(file_path):
#         with open(file_path, 'rb') as fh:
#             response = HttpResponse(fh.read(), content_type="application/x-python")
#             response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
#             return response
