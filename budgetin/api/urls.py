from django.urls import path

from api import views

app_name = 'api'

urlpatterns = [
    path('biro/', views.BiroView.as_view()),
    path('login/', views.LoginView.as_view()),
    path('login/user/', views.LoginUserView.as_view()),
    path('logout/', views.LogoutView.as_view()),
    path('test/', views.TestView.as_view()),
    path('import/list_planning/', views.ImportListPlanning.as_view()),
    path('download_list_planning/', views.ExportListPlanning.as_view()),
    path('download_list_project/', views.ExportListProject.as_view()),
    path('list_planning/', views.CreateListPlanning.as_view()),
]
