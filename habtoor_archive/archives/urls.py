from django.contrib import admin
from django.urls import path
from .views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('' , index , name='home'),
    path('dashboard' , dashboard , name='dashboard'),
    path('login/' , login_view , name='login'),
    path('logout/' , logout_view , name='logout'),
    path('article-types/' , manage_article_type , name='list_article_types'),
    path('article-types/edit/<int:pk>/', manage_article_type, name='update_article_type'),
    path('article-types/delete/<int:pk>/', delete_article_type, name='delete_article_type'),
]