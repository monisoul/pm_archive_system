from django import forms 
from django.forms import inlineformset_factory
from django.contrib.contenttypes.forms import generic_inlineformset_factory
from .models import *
from django.core.exceptions import ValidationError


class LoginForm(forms.Form):
    username = forms.CharField(
        max_length=150,
        required=True,
       
        )
    password = forms.CharField(
        required=True,       
    )

class ArticleTypeForm(forms.ModelForm):
    class Meta:
        model = ArticleType
        fields = ['name_ar']
        labels = {
            'name_ar': 'الاسم بالعربي',
            'name_en': 'الاسم بالانجليزي',
            
        }
        widgets = {
            'name_ar' : forms.TextInput(attrs={'class':'form-control' , 'placeholder':'أدخل اسم النوع'}),
            'name_en' : forms.TextInput(attrs={'class':'form-control' , 'placeholder':'أدخل اسم النوع بالانجليزي'}),
         
        }
        error_messages = {
            'name_ar': {
                'required': 'يرجى إدخال اسم نوع المقال.',        # Required
                'unique': 'اسم نوع المقال هذا موجود بالفعل.',   # Unique
                'max_length': 'اسم نوع المقال طويل جدًا، الحد الأقصى 100 حرف.'  # Max length
            }
        }

class CareerStageForm(forms.ModelForm):
    class Meta:
        model = CareerStage
        fields = ['name_ar' , 'start_date' ,'end_date' ,'description']
        error_messages = {
            'name_ar': {
                'required': 'يرجى إدخال اسم المرحلة.',        # Required
                'unique': 'اسم المرحلة هذا موجود بالفعل.',   # Unique
                'max_length': 'اسم المرحلة طويل جدًا، الحد الأقصى 100 حرف.'  # Max length
            }
        }
        
class AuthorityTypeForm(forms.ModelForm):
   class Meta:
        model = AuthorityType
        fields = ['name_ar']
        widgets = {
            'name_ar' : forms.TextInput(attrs={'class':'form-control' }),
            'name_en' : forms.TextInput(attrs={'class':'form-control'})
        }
        error_messages = {
            'name_ar': {
                'required': 'يرجى إدخال اسم نوع الجهة.',        # Required
                'unique': 'اسم نوع الجهة هذا موجود بالفعل.',   # Unique
                'max_length': 'اسم نوع الجهة طويل جدًا، الحد الأقصى 100 حرف.'  # Max length
            }
        }
        
class CategoryForm(forms.ModelForm):
   class Meta:
        model = Category
        fields = ['name_ar','description']
        widgets = {
            'name_ar' : forms.TextInput(attrs={'class':'form-control'}),
            'name_en' : forms.TextInput(attrs={'class':'form-control'})
        }
        error_messages = {
            'name_ar': {
                'required': 'يرجى إدخال اسم الصنف.',        # Required
                'unique': 'اسم الصنف هذا موجود بالفعل.',   # Unique
                'max_length': 'اسم الصنف طويل جدًا، الحد الأقصى 100 حرف.'  # Max length
            }
        }
        
        
class AuthorityForm(forms.ModelForm):
   class Meta:
        model = Authority
        fields = ['name_ar','type','location']
        widgets = {
            'name_ar' : forms.TextInput(attrs={'class':'form-control' , 'placeholder':'أدخل اسم الجهة'}),
            'name_en' : forms.TextInput(attrs={'class':'form-control' , 'placeholder':'أدخل اسم الجهة'})
        }
        error_messages = {
            'name_ar': {
                'required': 'يرجى إدخال اسم الجهة.',        # Required
                'unique': 'اسم الجهة هذا موجود بالفعل.',   # Unique
                'max_length': 'اسم الجهة طويل جدًا، الحد الأقصى 100 حرف.'  # Max length
            }
        }
        
class GeographicalLocationForm(forms.ModelForm):
    class Meta:
        model = GeographicalLocation
        fields = ['name_ar'  , 'type']
        widgets = {
            'name_ar' : forms.TextInput(attrs={'class':'form-control' }),
            'name_en' : forms.TextInput(attrs={'class':'form-control' })
        }
        error_messages = {
            'name_ar': {
                'required': 'يرجى إدخال اسم الموقع.',        # Required
                'unique': 'اسم الموقع هذا موجود بالفعل.',   # Unique
                'max_length': 'اسم الموقع طويل جدًا، الحد الأقصى 100 حرف.'  # Max length
            }
        }
        
class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ['title_ar' ,'article_date','content','Authority','type','category',
                'language','is_archived' ,'keywords']
       
        
    def clean(self):
        """      يقوم بفحص ما إذا كانت المقالة موجودة بالفعل بنفس العنوان والتاريخ والمحتوى.
        """
        cleaned_data = super().clean()
        
        # 1. استرجاع البيانات التي تم تنظيفها
        title = cleaned_data.get('title_ar')
        content = cleaned_data.get('content')
        publish_date = cleaned_data.get('publish_date')
        
        # 2. التحقق من وجود جميع الحقول المطلوبة للمقارنة
        if title and content and publish_date:
            
            # 3. بناء استعلام البحث عن مقالات مطابقة
            # ملاحظة: نستخدم تاريخ الإنشاء فقط (created_at) في المقارنة
            query = Article.objects.filter(
                title_ar__iexact=title, # المقارنة بدون حساسية لحالة الأحرف
                content__iexact=content, 
                publish_date__date=publish_date.date() # المقارنة بتاريخ الإنشاء فقط (اليوم والشهر والسنة)
            )

            # 4. استثناء الكائن الحالي إذا كنا في وضع التعديل (Update)
            # إذا كان النموذج مرتبطًا بكائن موجود (أي لديه PK)، نستثنيه من البحث
            if self.instance.pk:
                query = query.exclude(pk=self.instance.pk)

            # 5. إذا تم العثور على أي مقال مطابق
            if query.exists():
                # إطلاق خطأ تحقق عام على النموذج
                raise ValidationError("المقالة موجودة بالفعل بنفس العنوان والمحتوى وتاريخ الإنشاء.")
                
        return cleaned_data



class AttachmentForm(forms.ModelForm):
    # الإصلاح الرئيسي: تعيين ID كحقل غير مطلوب (required=False) 
    # هذا يحل مشكلة "This field is required" للحقل id 
    id = forms.IntegerField(widget=forms.HiddenInput(), required=False) 
    original_name = forms.CharField(widget=forms.HiddenInput(), required=False)

    class Meta:
        model = Attachment
        # يجب إدراج الحقل 'id' هنا أو في قائمة 'fields'
        fields = ('id', 'file', 'is_url', 'can_be_shared' , 'original_name') 
        # تأكد من أن هذه الحقول تناسب موديل Attachment الخاص بك
        # exclude = ('object_id', 'content_type', 'created_by') # يمكنك استخدام

#  استخدام Generic Inline Formset
# لا نحدد هنا المودل الأب، بل نحدد المودل الابن (Attachment)
AttachmentFormSet = generic_inlineformset_factory(
    Attachment, 
    form=AttachmentForm,
    fields=('file', 'is_url', 'can_be_shared'),
    extra=2,
    can_delete=True
)

class PublicationPlatformTypeForm(forms.ModelForm):
   class Meta:
        model = PublicationPlatformType
        fields = ['name_ar','code']
        widgets = {
            'name_ar' : forms.TextInput(attrs={'class':'form-control'}),
        }
        error_messages = {
            'name_ar': {
                'required': 'يرجى إدخال اسم نوع المنصة.',        
                'unique': 'اسم نوع المنصة هذا موجود بالفعل.',  
                'max_length': 'اسم نوع المنصة طويل جدًا، الحد الأقصى 100 حرف.'  
            },
            'code':{
                
                'required': 'يرجى إدخال اسم نوع المنصة.',        
                'unique': 'اسم نوع المنصة هذا موجود بالفعل.',  
                'max_length': 'اسم نوع المنصة طويل جدًا، الحد الأقصى 100 حرف.'  
            }
        }
        
class PublicationPlatformForm(forms.ModelForm):
   class Meta:
        model = PublicationPlatform
        fields = ['name_ar' , 'type']
        widgets = {
            'name_ar' : forms.TextInput(attrs={'class':'form-control'}),
        }
        error_messages = {
            'name_ar': {
                'required': 'يرجى إدخال اسم نوع المنصة.',        
                'unique': 'اسم نوع المنصة هذا موجود بالفعل.',  
                'max_length': 'اسم نوع المنصة طويل جدًا، الحد الأقصى 100 حرف.'  
            },
            'type': {
                'required': 'يرجى اختيار نوع المنصة.',
            },
            # هذا الجزء هو المسؤول عن رسالة الخطأ عند تكرار (الاسم + النوع)
            '__all__': {
                'unique_together': 'عذراً، هذه المنصة مسجلة مسبقاً بهذا النوع المحدد.',
            }
        }



class PublicationForm(forms.ModelForm):
    

    class Meta:
        model = Publication
        fields = ['platform', 'publish_date',  
            'website_url',
            'video_url',
            'book_title',
            'issue_number',
            'issue_date',
            'page_number',
           'page_image',
            'cover_image',
            'notes']
        
        widgets = {
            'publish_date': forms.DateInput(attrs={'type': 'date'}),
            'issue_date': forms.DateInput(attrs={'type': 'date'}),
        }

    

    
PublicationFormSet = generic_inlineformset_factory(
    Publication,
    form=PublicationForm,
    extra=3,
    can_delete=True
)
        

    
