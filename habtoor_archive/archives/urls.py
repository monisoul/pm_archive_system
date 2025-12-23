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
    # المسارات الاساسية للنافذة الرئيسية و شاشة الدخول
     path('admin/', admin.site.urls),
    path('' , index , name='home'),
    path('dashboard' , dashboard , name='dashboard'),
    path('login/' , login_view , name='login'),
    path('logout/' , logout_view , name='logout'),
 
 # مسارات انواع المقالات
    path('article/types/', ArticleTypeListView.as_view(), name='articletype-list'),
    path('article/types/create/',ArticleTypeCreateView.as_view(), name='articletype-create'),
    path('article/types/update/<int:pk>/', ArticleTypeUpdateView.as_view(), name='articletype-update'),
    path('article/types/delete/<int:pk>/', ArticleTypeDeleteView.as_view(), name='articletype-delete'),
    path('article/types/<int:pk>/detail/', ArticleTypeDetailView.as_view(), name='articletype-detail'),
    
    # مسارات تصنيف المقالات
    path('categories/', CategoryListView.as_view(), name='category-list'),
    path('categories/create/',CategoryCreateView.as_view(), name='category-create'),
    path('categories/update/<int:pk>/', CategoryUpdateView.as_view(), name='category-update'),
    path('categories/delete/<int:pk>/', CategoryDeleteView.as_view(), name='category-delete'),
    path('categories/<int:pk>/detail/', CategoryDetailView.as_view(), name='category-detail'),
    
     # مسارات انواع الجهات
    path('authority/types/', AuthorityTypeListView.as_view(), name='authoritytype-list'),
    path('authority/types/create/', AuthorityTypeCreateView.as_view(), name='authoritytype-create'),
    path('authority/types/update/<int:pk>/', AuthorityTypeUpdateView.as_view(), name='authoritytype-update'),
    path('authority/types/delete/<int:pk>/', AuthorityTypeDeleteView.as_view(), name='authoritytype-delete'),
    path('authority/types/<int:pk>/detail/', AuthorityTypeDetailView.as_view(), name='authoritytype-detail'),
    
    # مسارات المواقع الجغرافية  
    path('geographicallocation/', GeographicalLocationListView.as_view(), name='geographicallocation-list'),
    path('geographicallocation/create/', GeographicalLocationCreateView.as_view(), name='geographicallocation-create'),
    path('geographicallocation/update/<int:pk>/', GeographicalLocationUpdateView.as_view(), name='geographicallocation-update'),
    path('geographicallocation/delete/<int:pk>/', GeographicalLocationDeleteView.as_view(), name='geographicallocation-delete'),
    path('geographicallocation/<int:pk>/detail/', GeographicalLocationDetailView.as_view(), name='geographicallocation-detail'),
    
    # مسارات المراحل المهنية
    
    path('career/stages/', CareerStageListView.as_view(), name='careerstage-list'),
    path('career/stages/create/',CareerStageCreateView.as_view(), name='careerstage-create'),
    path('career/stages/update/<int:pk>/', CareerStageUpdateView.as_view(), name='careerstage-update'),
    path('career/stages/delete/<int:pk>/', CareerStageDeleteView.as_view(), name='careerstage-delete'),
    path('career/stages/<int:pk>/detail/', CareerStageDetailView.as_view(), name='careerstage-detail'),
    
 # مسارات الجهات  
    path('authority/', AuthorityListView.as_view(), name='authority-list'),
    path('authority/create/', AuthorityCreateView.as_view(), name='authority-create'),
    path('authority/update/<int:pk>/', AuthorityUpdateView.as_view(), name='authority-update'),
    path('authority/delete/<int:pk>/', AuthorityDeleteView.as_view(), name='authority-delete'),
    path('authority/<int:pk>/detail/', AuthorityDetailView.as_view(), name='authority-detail'),
    
# مسارات المقالات
    path('article/', ArticleListView.as_view(), name='article-list'),
    path('article/create/', ArticleCreateView.as_view(), name='article-create'),
    path('article/update/<int:pk>/', ArticleUpdateView.as_view(), name='article-update'),
    path('article/delete/<int:pk>/', ArticleDeleteView.as_view(), name='article-delete'),
   path('article/<int:pk>/detail/', ArticleDetailView.as_view(), name='article-detail'),
   
# مسارات انواع منصات النشر  
    path('publicationplatformtype/', PublicationPlatformTypeListView.as_view(), name='publicationplatformtype-list'),  
    path('publicationplatformtype/create/', PublicationPlatformTypeCreateView.as_view(), name='publicationplatformtype-create'),
    path('publicationplatformtype/update/<int:pk>/', PublicationPlatformTypeUpdateView.as_view(), name='publicationplatformtype-update'),
    path('publicationplatformtype/delete/<int:pk>/', PublicationPlatformTypeDeleteView.as_view(), name='publicationplatformtype-delete'),
    path('publicationplatformtype/<int:pk>/detail/', PublicationPlatformTypeDetailView.as_view(), name='publicationplatformtype-detail'),
    
    
    # مسارات منصات النشر  
    path('publicationplatform/', PublicationPlatformListView.as_view(), name='publicationplatform-list'),  
    path('publicationplatform/create/', PublicationPlatformCreateView.as_view(), name='publicationplatform-create'),
    path('publicationplatform/update/<int:pk>/', PublicationPlatformUpdateView.as_view(), name='publicationplatform-update'),
    path('publicationplatform/delete/<int:pk>/', PublicationPlatformDeleteView.as_view(), name='publicationplatform-delete'),
    path('publicationplatform/<int:pk>/detail/', PublicationPlatformDetailView.as_view(), name='publicationplatform-detail'),
    
    

   
    
    
]