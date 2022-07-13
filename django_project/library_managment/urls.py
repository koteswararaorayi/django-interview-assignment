from django.urls import path, include
from . import user_view

app_name = "library_managment"

urlpatterns = [
    path('signup', user_view.SignupView.as_view()),
]