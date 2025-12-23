from django.db import models
from django.core.validators import RegexValidator # لاستخدام التعبيرات القياسية
from django.contrib.auth.models import User
from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
import os
from django.db.models import Q
import uuid
from django.utils import timezone
from django.contrib.contenttypes.fields import GenericRelation
from django.contrib.auth.mixins import LoginRequiredMixin

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

# غير مستخدمة def publication_media_upload_path(instance, filename):
def publication_media_upload_path(instance, filename):
        date_path = timezone.now().strftime('%Y/%m/%d')
        ext = os.path.splitext(filename)[1]
        name = f"{uuid.uuid4().hex[:10]}{ext}"
        return f"publications/{date_path}/{name}"

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
    name_ar = models.CharField(max_length=191 , unique=True , verbose_name="المرحلة")
    name_en = models.CharField(max_length=191  , null=True , blank=True)
    description = models.TextField(null=True , blank=True)  
    start_date = models.DateField(verbose_name="تاريخ البدء", default=timezone.now)
    end_date = models.DateField(verbose_name="تاريخ الانتهاء", null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'المرحلة العملية'
        verbose_name_plural = 'المراحل العملية'
    
    def __str__(self):
        return str(self.name_ar)
    
class GeographicalLocation(models.Model):
    name_ar = models.CharField(max_length=100, unique=True , null=True , blank= True , verbose_name="الموقع")
    name_en = models.CharField(max_length=100, unique=True , null=True , blank= True) 
    type = models.CharField(max_length=100 , choices=[
        ('محافظة' ,'محافظة') , ('مديرية','مديرية') , ('مدينة','مدينة'),('دولة','دولة') ])
        
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'الموقع'
        verbose_name_plural = 'المواقع الجغرافية'

    def __str__(self):
        return self.name_ar  
    
class AuthorityType(models.Model):
    """مثال: "جامعة" / "مؤسسة تعليمية / جهة خاصة"
    """
    name_ar = models.CharField(max_length=191 , unique=True , verbose_name="نوع الجهة") 
    name_en = models.CharField(max_length=191 , null=True , blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'نوع الجهة'
        verbose_name_plural = 'انواع الجهة'
    
    def __str__(self):
        return str(self.name_ar)
    
    
class Authority(models.Model):
    name_ar = models.CharField(max_length=191 , unique=True , verbose_name="الجهة") 
    name_en = models.CharField(max_length=191 , null=True , blank=True)
    type = models.ForeignKey(AuthorityType , on_delete=models.SET_NULL ,null=True , blank= True , verbose_name="نوع الجهة" )
    location = models.ForeignKey(GeographicalLocation , on_delete=models.SET_NULL ,null=True , blank= True , verbose_name="الموقع"  )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    DETAIL_RELATIONS = {
        'type': [],
        'location': [],
    }
    
    class Meta:
        verbose_name = 'الجهة'
        verbose_name_plural = 'الجهات'
    
    def __str__(self):
        return str(self.name_ar)
    
class Category(models.Model):
    name_ar = models.CharField(max_length=255)
    name_en = models.CharField(max_length=191 , null=True , blank=True)
    #slug = models.SlugField(unique=True)
    description = models.TextField(null=True, blank=True)

    class Meta:
        verbose_name = "التصنيف"
        verbose_name_plural = "التصنيفات"

    def __str__(self):
        return self.name_ar
    

 
class Article(models.Model):
    title_ar = models.CharField(max_length=191  , verbose_name="عنوان المقال")
    title_en = models.CharField(max_length=191 , null=True , blank=True)
    content = models.TextField(verbose_name="محتوى المقال")
    Authority = models.ForeignKey(Authority , on_delete=models.SET_NULL , null=True , blank= True , verbose_name="الجهة/المؤسسة")
    article_date = models.DateField(
        verbose_name="تاريخ المقالة", 
        default=timezone.now
    )
    #publish_date = models.DateTimeField(verbose_name="تاريخ النشر")
    #status = models.CharField(max_length=20 , choices=[('مسودة' ,'مسودة') , ('معتمد','معتمد') , ('منشور','منشور'),('ملغي','ملغي')], default='معتمد' , verbose_name="حالة المقال")
        
    
    type = models.ForeignKey(ArticleType , on_delete=models.SET_NULL , null=True , blank= True , verbose_name="نوع المقال")
    category = models.ForeignKey(Category , on_delete=models.SET_NULL , null=True , blank= True , verbose_name="التصنيف")
   
    language = models.CharField(max_length=50 , choices=[
          ('ar' ,'عربي') , ('en','انجليزي')
        
    ] , default='ar' , verbose_name="اللغة")
    created_by = models.ForeignKey('auth.User' , on_delete=models.CASCADE , null=True, blank=True , verbose_name="انشأت بواسطة" )
    #approval_date = models.DateTimeField(null=True , blank= True , verbose_name="ـاريخ المصادقة")
    is_archived = models.BooleanField(null=True , default=False , blank= True , verbose_name="هل مؤرشف")
    career_stage = models.ForeignKey(CareerStage , on_delete=models.SET_NULL , null=True , blank= True , verbose_name="المرحلة العلمية المرتبطة")
    keywords = models.JSONField(null=True, blank=True)   #عدن, جامعة عدن, دكاترة الجامعة
    created_at = models.DateTimeField(auto_now_add=True , verbose_name="تاريخ الانشاء")
    updated_at = models.DateTimeField(auto_now=True , verbose_name="تاريخ آخر تعديل")
    
    attachments = GenericRelation('Attachment', related_query_name='article')
    publications = GenericRelation('Publication', related_query_name='article')
    
    DETAIL_RELATIONS = {
        'Authority': ['type', 'location'],
        'category': [],
        'career_stage': [],
    }
    
    class Meta:
        verbose_name = 'المقالة'
        verbose_name_plural = 'المقالات'
        
    def save(self, *args, **kwargs):
        # 1. إذا كان تاريخ المقالة متوفرًا
        if self.article_date:
            
            # 2. البحث عن المرحلة المهنية المطابقة
            # البحث عن المراحل التي:
            #   أ. تبدأ قبل أو في تاريخ المقالة (start_date <= article_date)
            #   ب. تنتهي بعد تاريخ المقالة (end_date >= article_date) أو لم تنته بعد (end_date is NULL)
            
            matching_stage = CareerStage.objects.filter(
                Q(start_date__lte=self.article_date),
                Q(end_date__gte=self.article_date) | Q(end_date__isnull=True)
            ).order_by('-start_date').first() 
            # نستخدم order_by('-start_date') في حالة تداخل التواريخ لضمان اختيار الأحدث أو الأكثر تحديدًا.

            # 3. تعيين المرحلة إذا وجدت
            if matching_stage:
                self.career_stage = matching_stage
            else:
                self.career_stage = None # أو يمكنك ترك الحقل كما هو إذا كان هناك قيمة سابقة

        # 4. حفظ الكائن
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.title_ar
    
    
# def attachment_upload_path(instance, filename):
#     """
#     تحديد مسار رفع الملف بناءً على اسم الجدول المرتبط
#     وتبسيط اسم الملف المحفوظ ليكون فريدًا وقصيرًا.
#     """
    
#     # 1. تحديد اسم النموذج و التأكد من أن الكائن مرتبط (لضمان المسار)
#     model_name = instance.content_object._meta.model_name if instance.content_object else 'temp_attachments'
#     safe_model_name = model_name.lower().replace('-', '_')

#     # 2. تحديد مجلد التاريخ
#     current_date = timezone.now().strftime('%Y/%m/%d')

#     # 3. فصل الامتداد وتوليد اسم ملف جديد وقصير
    
#     # الحصول على الامتداد (مثل '.png', '.pdf')
#     name, ext = os.path.splitext(filename)
    
#     # توليد معرّف فريد (UUID) لاسم الملف
#     unique_filename = f"{uuid.uuid4().hex[:10]}{ext}" # استخدام جزء من UUID + الامتداد

#     # إذا كان الكائن الأم محفوظاً بالفعل، نستخدم ID الكائن للحفظ النهائي
#     if instance.content_object and instance.content_object.pk:
#         # إذا تم الحفظ، نستخدم PK كجزء من الاسم لزيادة الوضوح
#         unique_filename = f"{instance.content_object.pk}_{uuid.uuid4().hex[:8]}{ext}"
    
#     # 4. بناء المسار النهائي
#     # المسار: attachments/اسم_النموذج/السنة/الشهر/اليوم/اسم_الملف_الفريد.ext
#     final_path = os.path.join(
#         f'attachments/{safe_model_name}/{current_date}', 
#         unique_filename
#     )
    
#     return final_path

def attachment_upload_path(instance, filename):
    model_name = instance.content_object._meta.model_name if instance.content_object else 'unknown'
    date_path = timezone.now().strftime('%Y/%m/%d')
    ext = os.path.splitext(filename)[1]
    name = f"{uuid.uuid4().hex[:10]}{ext}"

    return f"attachments/{model_name}/{date_path}/{name}"

def publication_upload_path(instance, filename):
    model_name = instance.content_object._meta.model_name if instance.content_object else 'unknown'
    date_path = timezone.now().strftime('%Y/%m/%d')
    ext = os.path.splitext(filename)[1]
    name = f"{uuid.uuid4().hex[:10]}{ext}"
    return f"publications/{model_name}/{date_path}/{name}"





class Attachment(models.Model):
    #  1. الحقول العامة للمفاتيح الخارجية (Generic Foreign Key)
    # لتحديد الجدول الذي ينتمي إليه المرفق (Article, Interview, etc.)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    # لتخزين رقم الكائن (ID) المرتبط في الجدول المحدد
    object_id = models.PositiveIntegerField(verbose_name="رقم المصدر")
    # الحقل الذي يجمع بين content_type و object_id للوصول إلى الكائن مباشرة
    content_object = GenericForeignKey('content_type', 'object_id' )
    
    
    #  2. حقل الملف 
    file = models.FileField(
        upload_to=attachment_upload_path, 
        max_length=191,
        verbose_name="الملف/المرفق",
        blank=True,
        null=True
    )
    original_name = models.CharField(max_length=255, blank=True  , null=True )
    
    #  3. الحقول الوصفية (نحتفظ بها كما هي) 
    is_url = models.BooleanField(default=False, verbose_name="مسار خارجي (رابط)")
    can_be_shared = models.BooleanField(default=True, verbose_name="هل ممكن مشاركته") 
    
    created_by = models.ForeignKey('auth.User',null=True,blank=True , on_delete=models.CASCADE, verbose_name="أُنشى بواسطة")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاريخ الانشاء")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="تاريخ آخر تعديل")
    
    def save(self, *args, **kwargs):
        if self.file:
            new_name = os.path.basename(self.file.name)

            if self.original_name != new_name:
                self.original_name = new_name

        super().save(*args, **kwargs)
    
    class Meta:
        verbose_name = 'المرفق'
        verbose_name_plural = 'المرفقات'
    
    def __str__(self):
        return self.file.name
    
class PublicationPlatformType(models.Model):
    """
    مثال:
    - موقع إلكتروني
    - كتاب
    - صحيفة/مجلة
    - قناة يوتيوب
    - قناة تلفزيونية /اذاعية
    """
    name_ar = models.CharField(max_length=191, unique=True, verbose_name="نوع المنصة")
    #name_en = models.CharField(max_length=191, null=True, blank=True)
    code = models.CharField(max_length=50, unique=True, null=True , blank=True ,verbose_name="رمز المنصة")
    created_at = models.DateTimeField(auto_now_add=True , verbose_name="تاريخ الانشاء")
    updated_at = models.DateTimeField(auto_now=True , verbose_name="تاريخ آخر تعديل")
    

    class Meta:
        verbose_name = "نوع منصة النشر"
        verbose_name_plural = "أنواع منصات النشر"

    def __str__(self):
        return self.name_ar

class PublicationPlatform(models.Model):
    name_ar = models.CharField(max_length=191, verbose_name="اسم المنصة")
    type = models.ForeignKey(
        PublicationPlatformType,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="نوع المنصة"
    )
    
    created_at = models.DateTimeField(auto_now_add=True , verbose_name="تاريخ الانشاء") 
    updated_at = models.DateTimeField(auto_now=True , verbose_name="تاريخ آخر تعديل")

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['name_ar', 'type'], 
                name='unique_platform_name_per_type'
            )
        ]
        verbose_name = "منصة نشر"
        verbose_name_plural = "منصات النشر"

    def __str__(self):
        return self.name_ar


class Publication(models.Model):
    #  Generic Relation
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField(verbose_name="رقم المصدر")
    content_object = GenericForeignKey('content_type', 'object_id')

    #  بيانات النشر
    # اسم المنصة 
    platform = models.ForeignKey(
        PublicationPlatform,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="منصة النشر"
    )
 
    publish_date = models.DateField(
        null=True,
        blank=True,
        verbose_name="تاريخ النشر"
    )

    
    page_image = models.FileField(
        upload_to=publication_upload_path,
        null=True,
        blank=True,
        verbose_name="صورة الصفحة"
    )

    cover_image = models.FileField(
        upload_to=publication_upload_path,
        null=True,
        blank=True,
        verbose_name="صورة الغلاف"
    )

    page_image_original_name = models.CharField(
        max_length=255, null=True, blank=True
    )
    cover_image_original_name = models.CharField(
        max_length=255, null=True, blank=True
    )
    page_number = models.CharField(
        max_length=50, null=True, blank=True, verbose_name="رقم الصفحة"
    )
    issue_number = models.CharField(
        max_length=50, null=True, blank=True, verbose_name="العدد للصحيفة"
    )

    issue_date  = models.DateField(
        null=True, blank=True, verbose_name="التاريخ للصحيفة"
    )
    
    website_url = models.URLField(
        
        null=True, blank=True, verbose_name="رابط الموقع"
        
    )
    book_title = models.CharField(
        max_length=255, null=True, blank=True, verbose_name="اسم الكتاب"
    )
    
    video_url = models.URLField(
        null=True, blank=True, verbose_name="رابط الفيديو"
    )


    notes = models.TextField(
        blank=True,
        null=True,
        verbose_name="ملاحظات"
    )


    created_by = models.ForeignKey(
        'auth.User',
        on_delete=models.CASCADE,null=True , blank= True ,
        verbose_name="أُنشئ بواسطة"
    )

    created_at = models.DateTimeField(auto_now_add=True , verbose_name="تاريخ الانشاء") 
    updated_at = models.DateTimeField(auto_now=True , verbose_name="تاريخ آخر تعديل")
    
    def save(self, *args, **kwargs):
        # --- صفحة ---
        if self.pk:
            # جلب النسخة القديمة من DB
            old = Publication.objects.filter(pk=self.pk).first()
        else:
            old = None

        # --- صفحة ---
        if self.page_image:
            # تحديث الاسم الأصلي فقط إذا تغير الملف
            if not old or old.page_image != self.page_image:
                self.page_image_original_name = os.path.basename(self.page_image.name)

        # --- غلاف ---
        if self.cover_image:
            if not old or old.cover_image != self.cover_image:
                self.cover_image_original_name = os.path.basename(self.cover_image.name)

        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "نشر"
        verbose_name_plural = "النشر"

    def __str__(self):
        return f"{self.platform} - {self.publish_date}"

