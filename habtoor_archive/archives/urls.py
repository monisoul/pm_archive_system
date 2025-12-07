from django.contrib import admin
from django.urls import path
from .views import *
from .views import (
    ArticleTypeListView, ArticleTypeUpdateView, ArticleTypeDeleteView,
   
)
 #ArticleListView, ArticleUpdateView, ArticleDeleteView

"""urlpatterns = [
    path('admin/', admin.site.urls),
    path('' , index , name='home'),
    path('dashboard' , dashboard , name='dashboard'),
    path('login/' , login_view , name='login'),
    path('logout/' , logout_view , name='logout'),
    path('article-types/' , manage_article_type , name='list_article_types'),
    path('article-types/edit/<int:pk>/', manage_article_type, name='update_article_type'),
    path('article-types/delete/<int:pk>/', delete_article_type, name='delete_article_type'),
]"""


urlpatterns = [
     path('admin/', admin.site.urls),
    path('' , index , name='home'),
    path('dashboard' , dashboard , name='dashboard'),
    path('login/' , login_view , name='login'),
    path('logout/' , logout_view , name='logout'),
 
    path('article/types/', ArticleTypeListView.as_view(), name='articletype-list'),
    path('article/types/create/',ArticleTypeCreateView.as_view(), name='articletype-create'),
    path('article/types/update/<int:pk>/', ArticleTypeUpdateView.as_view(), name='articletype-update'),
    path('article/types/delete/<int:pk>/', ArticleTypeDeleteView.as_view(), name='articletype-delete'),
    
    
    path('career/stages/', CareerStageListView.as_view(), name='careerstage-list'),
    path('career/stages/create/',CareerStageCreateView.as_view(), name='careerstage-create'),
    path('career/stages/update/<int:pk>/', CareerStageUpdateView.as_view(), name='careerstage-update'),
    path('career/stages/delete/<int:pk>/', CareerStageDeleteView.as_view(), name='careerstage-delete'),

   
    
    
]