from django.urls import path

from Donation import views

urlpatterns = [
    path('success', views.donation_success, name='donation success'),
    path('canceled', views.donation_canceled, name='donation canceled'),
    path('PayPal_IPN', views.donation_listener, name='donation listener'),

]
