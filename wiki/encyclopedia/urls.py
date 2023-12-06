from django.urls import path

from . import views

app_name = 'wiki'

urlpatterns = [
    path("", views.index, name="index"),
    path("<str:title>", views.get_page, name="get_page"),
    path("search/", views.search, name="search"),
    path("conf/new-page/", views.new, name="new-page"),
    path("new_save/", views.new_save, name="new_save")
    
]
