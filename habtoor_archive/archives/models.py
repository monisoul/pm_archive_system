from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class ArticleType(models.Model):
    name_ar = models.CharField(max_length=191 , unique=True)
    name_en = models.CharField(max_length=191  , null=True , blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return str(self.name_ar)
    
class CareerStage(models.Model):
    name_ar = models.CharField(max_length=191 , unique=True)
    name_en = models.CharField(max_length=191  , null=True , blank=True)
    description = models.TextField(null=True , blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return str(self.name_ar)
    
class Authority(models.Model):
    name_ar = models.CharField(max_length=191 , unique=True)
    name_en = models.CharField(max_length=191 , null=True , blank=True)
    type = models.CharField(max_length= 20, choices = [
        ('حكومي' ,'حكومي') , ('خاص','خاص') , ('جمعية','جمعية')
        ] ,
        default='حكومي')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return str(self.name_ar)
    
class Governorate(models.Model):
    name_ar = models.CharField(max_length=100, unique=True , null=True , blank= True)
    name_en = models.CharField(max_length=100, unique=True , null=True , blank= True) # اسم المحافظة
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    
    
    
class Article(models.Model):
    title_ar = models.CharField(max_length=191 , unique=True)
    title_en = models.CharField(max_length=191)
    content = models.TextField()
    Authority = models.ForeignKey(Authority , on_delete=models.SET_NULL , null=True , blank= True)
    publish_date = models.DateTimeField()
    status = models.CharField(max_length=20 , choices=[
         ('مسودة' ,'مسودة') , ('معتمد','معتمد') , ('منشور','منشور'),('ملغي','ملغي')
        
    ], default='معتمد')
    article_type = models.ForeignKey(ArticleType , on_delete=models.SET_NULL , null=True , blank= True)
    category = models.CharField(max_length=100 , choices=[
        ('أخبار' ,'أخبار') , ('بيانات','بيانات') , ('مقالات','مقالات'),('رأي','رأي')
        
    ] , null=True , blank= True)
    language = models.CharField(max_length=50 , choices=[
          ('ar' ,'عربي') , ('en','انجليزي')
        
    ] , default='ar')
    approved_by = models.ForeignKey(User , on_delete=models.CASCADE , null=True , blank= True )
    approval_date = models.DateTimeField(null=True , blank= True)
    is_archived = models.BooleanField(null=True , blank= True)
    career_stage = models.ForeignKey(CareerStage , on_delete=models.SET_NULL , null=True , blank= True)
    is_national = models.BooleanField(default=False , null=True , blank= True)
    city = models.ForeignKey(Governorate , on_delete=models.CASCADE , null=True , blank= True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.title_ar
    
    
class Attachment(models.Model):
    file_name = models.CharField(max_length=191 , null=True , blank= True , unique=True)
    file_original_name = models.CharField(max_length=191 , null=True , blank= True , unique=True)
    source_table = models.CharField(max_length=191 , null=True , blank= True )
    source_type =  models.CharField(max_length=191 , null=True , blank= True )
    source_id = models.BigIntegerField()
    file_path = models.CharField(max_length=191)
    file_extension = models.CharField(max_length=191 , null=True , blank= True )
    is_url = models.BooleanField(default=False)
    can_be_shared = models.BooleanField(default=True)
    file_size = models.DecimalField(max_digits=10, decimal_places=2)
    created_by = models.ForeignKey(User , on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.file_name