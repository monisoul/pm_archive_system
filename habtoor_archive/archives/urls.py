from django.contrib import admin
from django.urls import path
from .views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('' , index , name='home'),
    path('dashboard' , dashboard , name='dashboard'),
    path('login/' , login_view , name='login'),
    path('logout/' , logout_view , name='logout'),
    path('create/article-type/' , create_article_type , name='create_article_type')
]