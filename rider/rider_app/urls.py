"""
    Url mappings for rider app
"""

from django.urls import path

from rider_app import views

urlpatterns = [
    path('create_ride/', views.create_ride, name='create_ride')
]
