from django.urls import path

from api import views

app_name = 'api'

urlpatterns = [
    path('ithc/biro/', views.BiroIthcView.as_view()),
    path('login/', views.LoginView.as_view()),
    path('login/user/', views.LoginUserView.as_view()),
    path('logout/', views.LogoutView.as_view()),
    path('test/', views.TestView.as_view()),
    path('import/list_planning/', views.ImportListPlanning.as_view()),
    path('import/realisasi/', views.ImportRealisasi.as_view()),
    path('download/list_budget/', views.ExportListBudget.as_view()),
    path('download_list_project/', views.ExportListProject.as_view())
]
