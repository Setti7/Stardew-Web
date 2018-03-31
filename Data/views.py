from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import UserDataForm
from .models import UserData
import numpy as np


@login_required
def ranking(request):
    submitted = ''
    if request.method == 'POST':
        form = UserDataForm(request.POST, request.FILES)

        file = request.FILES['file']
        submitted = 'False'
        if form.is_valid() and (file.name == 'training_data.npy') and (file.size > 100):
            score = len(list(np.load(file)))
            file = UserData(file=request.FILES['file'], user=request.user, score=score)
            file.save()
            submitted = 'True'
            redirect('ranking/')

    else:
        form = UserDataForm()
    return render(request, 'dashboard.html', context={
        'form': form,
        'submitted': submitted
    })
