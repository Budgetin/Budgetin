"""budgetin URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from api import views

router = routers.DefaultRouter()
router.register('api/budget', views.BudgetViewSet)
router.register('api/coa', views.CoaViewSet)
router.register('api/monitoring', views.MonitoringViewSet)
router.register('api/planning', views.PlanningViewSet)
router.register('api/product', views.ProductViewSet)
router.register('api/project', views.ProjectViewSet)
router.register('api/project_type', views.ProjectTypeViewSet)
router.register('api/user', views.UserViewSet)
router.register('api/strategy', views.StrategyViewSet)
router.register('api/auditlog', views.AuditLogViewSet)
router.register('api/biro', views.BiroViewSet)
router.register('api/project_detail', views.ProjectDetailViewSet)
router.register('api/mytask', views.TaskViewSet, 'mytask')

urlpatterns = [
    path('', include(router.urls)),
    path('api/', include('api.urls')),
    path('admin/', admin.site.urls),
]
