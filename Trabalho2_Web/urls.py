"""Trabalho2_Web URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from library import views

urlpatterns = [    
    path('', views.home, name='home'),
    
    path('admin/', admin.site.urls),
    
    path('book/all',views.book_all,name='book_all'),
    path('book/create',views.book_create,name='book_create'),
    path('book/<int:book_id>/update',views.book_update,name='book_update'),
    path('book/<int:book_id>/view',views.book_view,name='book_view'),
    path('book/<int:book_id>/delete',views.book_delete,name='book_delete'),
    
    path('author/all',views.author_all,name='author_all'),
    path('author/create',views.author_create,name='author_create'),
    path('author/<int:author_id>/update',views.author_update,name='author_update'),
    path('author/<int:author_id>/view',views.author_view,name='author_view'),
    path('author/<int:author_id>/delete',views.author_delete,name='author_delete'),
    
    path('user/create',views.user_create, name='user_create'),
    path('user/login/',views.user_login, name='user_login'),
    path('user/logout',views.user_logout, name='user_logout'),
    path('user/verify_username', views.user_verify_username, name='user_verify_username'),
    
    path('loan/<int:book_id>/do',views.loan_do, name='loan_do'),
    path('loan/<int:book_id>/undo',views.loan_undo, name='loan_undo'),    
]
