from django.conf.urls import url
from . import views

from django.contrib import admin
from django.urls import path, include
from rest_framework import routers

from .views import *


router = routers.DefaultRouter()
router.register(r'messages', AlertViewSet)
router.register(r'groups', GroupViewSet)
router.register(r'silence', SilenceInfoViewSet)
router.register(r'alert', AlertInfoViewSet)

urlpatterns = [
    url(r'^monitoring/alarm/', views.webhook, name='webhook'),
    url(r'^monitoring/web-alert/', views.web_alert, name='web_alert'),
    url(r'^monitoring/alarm-out/', views.alarm_out, name='alarm_out'),
    url(r'^monitoring/status/', views.get_alert_status, name='get_alert_status'),
    url(r'^monitoring/callstatus/', views.post_alert_status, name='post_alert_status'),

    # http://localhost:8000/
    path('', index_view, name='index'),

    # http://localhost:8000/api/<router-viewsets>
    path('api/', include(router.urls)),

    # http://localhost:8000/api/admin/
    path('api/admin/', admin.site.urls),

    url(r'^api/groups/(?P<pk>\d+)/edit/$', UpdateGroup.as_view(), name='update'),

    url(r'^api/silence/(?P<pk>\d+)/edit/$', SilenceInfoUpdate.as_view(), name='updatesilence'),
]