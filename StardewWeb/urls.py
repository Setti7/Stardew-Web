from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.shortcuts import render
from django.urls import path, include

import Data.views as data_views
from Account import views as account_views


def error_404(request):
    return render(request, '404.html')


def error_500(request):
    return render(request, '500.html')


def error_400(request):
    return render(request, '400.html')


def error_403(request):
    return render(request, '403.html')


urlpatterns = [
                  path('admin/', admin.site.urls, name='admin'),

                  path('', data_views.home_page, name='home page'),
                  path('ranking/', include('Data.urls'), name='ranking'),
                  path('api/', include('Api.urls'), name='api'),

                  # Removing unwanted options from django-allauth
                  path('accounts/password/set/', error_404),
                  path('accounts/password/change/', error_404),
                  path('accounts/signup/', error_404),
                  path('accounts/password/reset/', error_404),
                  path('accounts/email/', error_404),

                  # Redirecting cancelled logins to home page
                  path('accounts/social/login/cancelled/', account_views.login_cancelled),
                  path('accounts/', include('allauth.urls')),

                  path('404/', error_404),
                  path('500/', error_500),
                  path('400/', error_400),
                  path('403/', error_403),

                  path('donation/', include('Donation.urls')),

              ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

admin.site.site_header = "SVFB Admin"
admin.site.site_title = "SVFB Admin Portal"
admin.site.index_title = "Welcome to SVFB"



if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),

    ] + urlpatterns