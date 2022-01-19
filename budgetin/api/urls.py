from django.urls import path

from api import views

app_name = 'api'
urlpatterns = [
    path('/token', views.TokenView.as_view(), name='token')
]
