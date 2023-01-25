"""
    Url mappings for rider app
"""

from django.urls import path
from requester_app import views


urlpatterns = [
    path('create_request/', views.create_request, name='create_request'),
    path('get_requesters_request/<int:requester_id>/',views.get_requester_requests, name='get_requesters_request'),
    path('get_match/<str:request_id>/', views.get_match, name="get_match"),
    path('apply/', views.apply, name="apply")
]
