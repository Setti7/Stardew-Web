from django.shortcuts import render

def home_page(request):
    """
    View function for the home page
    """

    return render(request, 'home_page.html', context={})