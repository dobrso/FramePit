from django.urls import path
from django.views.generic import TemplateView

from .views import check_redis

app_name = 'main'

urlpatterns = [
    path('', TemplateView.as_view(template_name='main/home.html'), name='home'),
    path('check-redis/', check_redis, name='check_redis'),
]