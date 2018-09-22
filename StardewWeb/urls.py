from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, include
from django.views.generic import RedirectView

import Data.views as data_views
from StardewWeb import views as core_views

urlpatterns = [
    path('admin/', admin.site.urls, name='admin'),

    path('', RedirectView.as_view(url='/home')),
    path('home/', data_views.home_page, name='home page'),
    path('ranking/', include('Data.urls'), name='ranking'),
    path('api/', include('api.urls'), name='api'),

    path('accounts/', include('Account.urls'), name='account'),

    path('404/', core_views.error_404),
    path('500/', core_views.error_500),
    path('400/', core_views.error_400),
    path('403/', core_views.error_403),

    path('donation/success', core_views.donation_success),
    path('donation/canceled', core_views.donation_canceled),

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

admin.site.site_header = "SVFB Admin"
admin.site.site_title = "SVFB Admin Portal"
admin.site.index_title = "Welcome to SVFB"
