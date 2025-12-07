from django.db import models
from django.core.validators import RegexValidator # لاستخدام التعبيرات القياسية
from django.contrib.auth.models import User

# Create your models here.

# يمنع الأرقام ويسمح فقط بالحروف العربية والمسافات
arabic_chars_only = RegexValidator(
    r'^[\u0600-\u06FF\s]+$', # التعبير القياسي للحروف العربية والمسافات
    'يجب أن يحتوي الاسم بالعربي على حروف عربية ومسافات فقط.',
)

# يمنع الأرقام ويسمح فقط بالحروف الإنجليزية (كبيرة وصغيرة) والمسافات
english_chars_only = RegexValidator(
    r'^[a-zA-Z\s]+$', # التعبير القياسي للحروف الإنجليزية والمسافات
    'يجب أن يحتوي الاسم بالانجلزي  على حروف إنجليزية ومسافات فقط.',
)

class ArticleType(models.Model):
    name_ar = models.CharField(max_length=191 ,validators=[arabic_chars_only], unique=True , verbose_name="نوع المقالة")
    name_en = models.CharField(max_length=191 ,validators=[english_chars_only] , null=True , blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        #verbose_name = _('Article Type')
        #verbose_name_plural = _('Article Types')
        # أو استخدم اسم النماذج باللغة العربية مباشرة إذا كنت لا تخطط للغات أخرى
        verbose_name = 'نوع المقالة'
        verbose_name_plural = 'أنواع المقالات'
    
    def __str__(self):
        return str(self.name_ar)
    
class CareerStage(models.Model):
    name_ar = models.CharField(max_length=191 , unique=True , verbose_name="المهنة")
    name_en = models.CharField(max_length=191  , null=True , blank=True)
    description = models.TextField(null=True , blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'مرحلة المهنة'
        verbose_name_plural = 'مراحل المهنة'
    
    def __str__(self):
        return str(self.name_ar)
    
class Authority(models.Model):
    name_ar = models.CharField(max_length=191 , unique=True , verbose_name="الجهة") 
    name_en = models.CharField(max_length=191 , null=True , blank=True)
    type = models.CharField(max_length= 20, choices = [
        ('حكومي' ,'حكومي') , ('خاص','خاص') , ('جمعية','جمعية')
        ] ,
        default='حكومي')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'الجهة'
        verbose_name_plural = 'الجهات'
    
    def __str__(self):
        return str(self.name_ar)
    
class Governorate(models.Model):
    name_ar = models.CharField(max_length=100, unique=True , null=True , blank= True , verbose_name="المحافظة")
    name_en = models.CharField(max_length=100, unique=True , null=True , blank= True) # اسم المحافظة
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'المحافظة'
        verbose_name_plural = 'المحافظات'

    def __str__(self):
        return self.name
    
    
    
class Article(models.Model):
    title_ar = models.CharField(max_length=191 , unique=True , verbose_name="عنوان المقال")
    title_en = models.CharField(max_length=191)
    content = models.TextField(verbose_name="محتوى المقال")
    Authority = models.ForeignKey(Authority , on_delete=models.SET_NULL , null=True , blank= True , verbose_name="الجهة")
    publish_date = models.DateTimeField(verbose_name="تاريخ النشر")
    status = models.CharField(max_length=20 , choices=[
         ('مسودة' ,'مسودة') , ('معتمد','معتمد') , ('منشور','منشور'),('ملغي','ملغي')
        
    ], default='معتمد' , verbose_name="حالة المقال")
    article_type = models.ForeignKey(ArticleType , on_delete=models.SET_NULL , null=True , blank= True , verbose_name="نوع المقال")
    category = models.CharField(max_length=100 , choices=[
        ('أخبار' ,'أخبار') , ('بيانات','بيانات') , ('مقالات','مقالات'),('رأي','رأي')
        
    ] , null=True , blank= True , verbose_name="تصنيف المقال")
    language = models.CharField(max_length=50 , choices=[
          ('ar' ,'عربي') , ('en','انجليزي')
        
    ] , default='ar' , verbose_name="اللغة")
    approved_by = models.ForeignKey(User , on_delete=models.CASCADE , null=True , blank= True , verbose_name="المصادقة بواسطة" )
    approval_date = models.DateTimeField(null=True , blank= True , verbose_name="ـاريخ المصادقة")
    is_archived = models.BooleanField(null=True , blank= True , verbose_name="هل مؤرشف")
    career_stage = models.ForeignKey(CareerStage , on_delete=models.SET_NULL , null=True , blank= True , verbose_name="المهنة التي كان يشغلها")
    is_national = models.BooleanField(default=False , null=True , blank= True , verbose_name="مقال وطني")
    city = models.ForeignKey(Governorate , on_delete=models.CASCADE , null=True , blank= True , verbose_name="المدينة")
    created_at = models.DateTimeField(auto_now_add=True , verbose_name="تاريخ الانشاء")
    updated_at = models.DateTimeField(auto_now=True , verbose_name="تاريخ آخر تعديل")
    
    class Meta:
        verbose_name = 'المقالة'
        verbose_name_plural = 'المقالات'
    
    def __str__(self):
        return self.title_ar
    
    
class Attachment(models.Model):
    file_name = models.CharField(max_length=191 , null=True , blank= True , unique=True , verbose_name="اسم الملف")
    file_original_name = models.CharField(max_length=191 , null=True , blank= True , unique=True , verbose_name="اسم الملف الاصلي")
    source_table = models.CharField(max_length=191 , null=True , blank= True , verbose_name="الجدول")
    source_type =  models.CharField(max_length=191 , null=True , blank= True , verbose_name="نوع المصدر" )
    source_id = models.BigIntegerField( verbose_name="رقم المصدر")
    file_path = models.CharField(max_length=191 , verbose_name="مسار الملف")
    file_extension = models.CharField(max_length=191 , null=True , blank= True , verbose_name="امتداد الملف")
    is_url = models.BooleanField(default=False , verbose_name="مسار خارجي")
    can_be_shared = models.BooleanField(default=True , verbose_name="هل ممكن مشاركته") 
    file_size = models.DecimalField(max_digits=10, decimal_places=2 , verbose_name="حجم الملف")
    created_by = models.ForeignKey(User , on_delete=models.CASCADE, verbose_name="أُنشى بواسطة")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاريخ الانشاء")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="تاريخ آخر تعديل")
    
    class Meta:
        verbose_name = 'المرفق'
        verbose_name_plural = 'المرفقات'
    
    def __str__(self):
        return self.file_name