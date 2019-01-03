from . import views
from django.urls import path
from rest_framework.authtoken import views as rest_views


urlpatterns = [
    path('check-score', views.score_check, name='api score'),
    path('version-control', views.version_control, name='api version control'),
    path('bug-report', views.bug_report, name='api bug report'),
    path('data-upload', views.data_upload, name='api data upload'),
    path('data-delete', views.data_delete, name='api data delete'),
    path('reset-token', views.reset_token, name='api reset token'),
    # path('download', views.download, name='update'),
    path('create-account', views.api_create_account, name='api create account'),
    path('validate-token', views.validate_token, name='api validate token'),
    path('get-token', rest_views.obtain_auth_token, name='api get token'),

]

