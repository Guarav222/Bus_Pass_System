"""BusPassSystem URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.urls import path
from buspass.views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index, name='index'),
    path('admin_home', admin_home, name='admin_home'),
    path('add_Category', add_Category, name='add_Category'),
    path('manage_Category', manage_Category, name='manage_Category'),
    path('edit_Category/<int:pid>', edit_Category, name='edit_Category'),
    path('delete_Category/<int:pid>', delete_Category, name='delete_Category'),
    path('add_Pass', add_Pass, name='add_Pass'),
    path('manage_Pass', manage_Pass, name='manage_Pass'),
    path('edit_Pass/<int:pid>', edit_Pass, name='edit_Pass'),
    path('view_PassDetails/<int:pid>', view_PassDetails, name='view_PassDetails'),
    path('delete_Pass/<int:pid>', delete_Pass, name='delete_Pass'),
    path('search',search, name='search'),
    path('betweendate_report',betweendate_report, name='betweendate_report'),
    path('changePassword', changePassword, name='changePassword'),
    path('logout/',Logout, name='logout'),
    path('contact', contact, name='contact'),
    path('pass_Enquiry', pass_Enquiry, name='pass_Enquiry'),
    path('view_PassEnquiryDtls/<int:pid>', view_PassEnquiryDtls, name='view_PassEnquiryDtls'),
    path('unread_queries', unread_queries, name='unread_queries'),
    path('read_queries', read_queries, name='read_queries'),
    path('view_queries/<int:pid>', view_queries, name='view_queries'),
    path('delete_contact/<int:pid>', delete_contact, name='delete_contact'),


]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
