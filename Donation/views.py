from django.shortcuts import render

# Create your views here.

def donation_listener(request):

    if request.method == 'POST':
        print("POST")
        print(request.POST)

    else:
        print("GET")
        print(request.GET)

    return render(request, '403.html')

def donation_success(request):
    return render(request, 'Donation/donation_success.html')


def donation_canceled(request):
    return render(request, 'Donation/donation_canceled.html')
