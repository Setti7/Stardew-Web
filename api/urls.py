from . import views
from django.urls import path

urlpatterns = [
    path('score', views.score, name='score'),
    path('version-control', views.version_control, name='version control'),
    path('bug-report', views.bug_report, name='bug report'),
    path('data-upload', views.data_upload, name='data upload'),
    path('login', views.api_login, name='api login'),
    # path('download', views.download, name='update'),
    path('create-account', views.api_create_account, name='api create account')

]



