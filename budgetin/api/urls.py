from django.urls import path

from api import views

app_name = 'api'

urlpatterns = [
    path('ithc/biro/', views.BiroIthcView.as_view()),
    path('login/', views.LoginView.as_view()),
    path('login/user/', views.LoginUserView.as_view()),
    path('logout/', views.LogoutView.as_view()),
    path('import/list_budget/', views.ImportListBudget.as_view()),
    path('import/dcsp/', views.ImportDCSP.as_view()),
    path('dashboard/group_budget/', views.GroupBudgetView.as_view()),
]
