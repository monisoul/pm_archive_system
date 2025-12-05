from django.contrib import admin
from django.urls import path
from .views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('' , index , name='home'),
    path('dashboard' , dashboard , name='dashboard'),
    path('login/' , login_view , name='login'),
    path('logout/' , logout_view , name='logout'),
    path('create/article-type/' , create_article_type , name='create_article_type'),
    path('article-type/<int:id>/', create_article_type, name='edit_article_type'),
    path('update/article-type/<int:pk>/', update_article_type, name='update_article_type'),
    path("delete-article-type/<int:id>/", delete_article_type, name="delete_article_type"),
]