"""
URL configuration for backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
import raw_data_verifier.views  as views


router = routers.DefaultRouter()
router.register(r"data_file_infos", views.DataFileInfoView, "Raw Data Verifier")
router.register(r"guid_lists", views.GuidListView, "GUID List")
router.register(r"patient_image_counts", views.PatientImageCountView, "Patient Image Count")

urlpatterns = [
    path('hello/', views.hello,name = 'hello'),
    path('homePage/', views.homePage, name='homePage'),
    path('api/data_delete/<path:file_path>/', views.delete_data_file_info, name='delete_data_file_info'),
    path('api/', include(router.urls)),
    path('api/cached-items/<str:data_type>', views.ServerConnectionsView.get_cached_items, name='cached-items'),
    path('api/handle-info-click/<path:itemPath>/<str:arrival_date_time>', views.handle_info_click, name='handle-info-click'),
]
