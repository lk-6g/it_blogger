from django.urls import path, re_path
from . import views

app_name = 'it_bloggers'

urlpatterns = [
    path('', views.index, name='index'),
    path('topics/', views.topics, name='topics'),
    path('new_topic/', views.new_topic, name='new_topic'),
    path('edit_topic/', views.edit_topic, name='edit_topic'),
    path('new_entry/', views.new_entry, name='new_entry'),
    path('edit_entry/<entry_id>/', views.edit_entry, name='edit_entry'),
    path('del_topic/', views.del_topic, name='del_topic'),
    path('del_entry/', views.del_entry, name='del_entry'),
    path('homepage/', views.homepage, name='homepage'),
    path('entries/', views.entries, name='entries'),
    path('entry/<entry_id>/', views.entry, name='entry'),
    path('increase_likes/<entry_id>/', views.increase_likes, name='increase_likes'),
    path('visitor/<owner_id>/', views.visitor, name='visitor'),
    ]