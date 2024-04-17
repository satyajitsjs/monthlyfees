"""
URL configuration for monthlyfees project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.urls import path,include
from admin_panel import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.Index_function , name="Index_function") ,
    
    
    path('login/', views.admin_login, name='admin_login'),
    path('logout/', views.admin_logout, name='admin_logout'),


    path('admin-dashboard/', views.admin_dashboard , name="admin_dashboard"),
    
    path('add/', views.add_institute, name='add_institute'),
    path('institute-list/', views.institute_list, name='institute_list'),
    path('view-institute/<str:institute_id>/', views.view_institute, name='view_institute'),
    path('edit-institute/<str:institute_id>/', views.edit_institute, name='edit_institute'),
    path('delete-institute/<str:institute_id>/', views.delete_institute, name='delete_institute'),
    
    
    
    path('institute/', include('institute_panel.urls')),
    
    
    
    path('institute_student_list/', views.institute_student_list, name='institute_student_list'),
    path('view_student_list/<str:institute_id>/', views.view_student_list, name='view_student_list'),
    path('view-student/<int:student_id>/', views.view_student_1, name='view_student3'),
    path('edit-student/<int:student_id>/', views.edit_student_list, name='edit_student3'),
    path('delete-student/<int:student_id>/', views.delete_student_list, name='delete_student3'),
    
    
    path('add-bse-fees/', views.add_bse_fees, name='add_bse_fees'),
    path('view-bse-fees/', views.view_bse_fees, name='view_bse_fees'),
    path('edit-bse-fee/<int:fee_id>/', views.edit_bse_fee, name='edit_bse_fee'),
    path('delete-bse-fee/<int:fee_id>/', views.delete_bse_fee, name='delete_bse_fee'),
    
    
    path('add-cbse-fees/', views.add_cbse_fees, name='add_cbse_fees'),
    path('view-cbse-fees/', views.view_cbse_fees, name='view_cbse_fees'),
    path('edit-cbse-fee/<int:fee_id>/', views.edit_cbse_fee, name='edit_cbse_fee'),
    path('delete-cbse-fee/<int:fee_id>/', views.delete_cbse_fee, name='delete_cbse_fee'),
    
    
    path('add-competitive-fees/', views.add_competitive_fees, name='add_competitive_fees'),
    path('view-competitive-fees/', views.view_competitive_fees, name='view_competitive_fees'),
    path('edit-competitive-fee/<int:fee_id>/', views.edit_competitive_fee, name='edit_competitive_fee'),
    path('delete-competitive-fee/<int:fee_id>/', views.delete_competitive_fee, name='delete_competitive_fee'),
    
    
    
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
