from django.conf.urls import include, url
from lists import views

urlpatterns = [
    url(r'^$', views.home_page, name='home'),
    url(r'^the-only-list-in-the-world/', views.view_list, name="view_list"),
    url(r'^new$', views.new_list, name='new_list')
]
