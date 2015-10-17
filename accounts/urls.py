from django.conf.urls import include, url
from accounts import views

urlpatterns = [
    url(r'^login$', views.persona_login, name='persona_login'),
]