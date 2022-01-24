from django.urls import path

from api import views

app_name = 'api'

urlpatterns = [
    path('login/', views.LoginView.as_view()),
    path('logout/', views.LogoutView.as_view()),
]
