from django.conf.urls import include, url
from accounts import views
from django.contrib.auth.views import logout

urlpatterns = [
    url(r'^login$', views.persona_login, name='persona_login'),
    url(r'^logout$', logout, {'next_page': '/lists/'}, name='logout'),
]