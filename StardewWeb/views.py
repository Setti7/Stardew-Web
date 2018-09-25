from django.shortcuts import render


def error_404(request):
    return render(request, '404.html')


def error_500(request):
    return render(request, '500.html')


def error_400(request):
    return render(request, '400.html')


def error_403(request):
    return render(request, '403.html')
