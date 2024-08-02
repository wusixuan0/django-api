from django.urls import path, include
from .views import HelloWorld, PersonListCreateView

urlpatterns = [
    path('hello/', HelloWorld.as_view(), name='hello_world'),
    path('persons/', PersonListCreateView.as_view(), name='person-list-create'),
]