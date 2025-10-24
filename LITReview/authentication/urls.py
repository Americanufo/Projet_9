from django.urls import path
from . import views

app_name = 'authentication'

urlpatterns = [
    path('', views.subscriptions, name='subscriptions'),
    path('unfollow/<int:followed_id>/', views.unfollow, name='unfollow'),
]
