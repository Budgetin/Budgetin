from django.urls import path

from api import views

app_name = 'api'

urlpatterns = [
    path('biro/', views.BiroView.as_view()),
    path('login/', views.LoginView.as_view()),
    path('logout/', views.LogoutView.as_view()),
    path('test/', views.TestView.as_view()),
    path('upload/', views.ImportExcelView.as_view()),
    path('download_list_planning/', views.ExportListPlanning.as_view()),
    path('download_list_project/', views.ExportListProject.as_view()),
]
