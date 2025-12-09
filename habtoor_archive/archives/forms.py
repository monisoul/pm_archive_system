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
        fields = ['name_ar', 'name_en']
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
                'unique': 'اسم النوع هذا موجود بالفعل.',   # Unique
                'max_length': 'اسم المحافظة طويل جدًا، الحد الأقصى 100 حرف.'  # Max length
            }
        }

class CareerStageForm(forms.ModelForm):
    class Meta:
        model = CareerStage
        fields = ['name_ar' , 'name_en','description']
        widgets = {
            'name_ar' : forms.TextInput(attrs={'class':'form-control' , 'placeholder':'أدخل اسم النوع'}),
            'name_en' : forms.TextInput(attrs={'class':'form-control' , 'placeholder':'أدخل اسم النوع'})
        }
        error_messages = {
            'name_ar': {
                'required': 'يرجى إدخال اسم المحافظة.',        # Required
                'unique': 'اسم المحافظة هذا موجود بالفعل.',   # Unique
                'max_length': 'اسم المحافظة طويل جدًا، الحد الأقصى 100 حرف.'  # Max length
            }
        }
        
class AuthorityForm(forms.ModelForm):
   class Meta:
        model = Authority
        fields = ['name_ar' , 'name_en','type']
        widgets = {
            'name_ar' : forms.TextInput(attrs={'class':'form-control' , 'placeholder':'أدخل اسم النوع'}),
            'name_en' : forms.TextInput(attrs={'class':'form-control' , 'placeholder':'أدخل اسم النوع'})
        }
        error_messages = {
            'name_ar': {
                'required': 'يرجى إدخال اسم المحافظة.',        # Required
                'unique': 'اسم المحافظة هذا موجود بالفعل.',   # Unique
                'max_length': 'اسم المحافظة طويل جدًا، الحد الأقصى 100 حرف.'  # Max length
            }
        }
        
class GovernorateForm(forms.ModelForm):
    class Meta:
        model = Governorate
        fields = ['name_ar' , 'name_en']
        widgets = {
            'name_ar' : forms.TextInput(attrs={'class':'form-control' , 'placeholder':'أدخل اسم النوع'}),
            'name_en' : forms.TextInput(attrs={'class':'form-control' , 'placeholder':'أدخل اسم النوع'})
        }
        error_messages = {
            'name_ar': {
                'required': 'يرجى إدخال اسم المحافظة.',        # Required
                'unique': 'اسم المحافظة هذا موجود بالفعل.',   # Unique
                'max_length': 'اسم المحافظة طويل جدًا، الحد الأقصى 100 حرف.'  # Max length
            }
        }
        
class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ['title_ar' , 'title_en','content','Authority','publish_date','status','article_type','category',
                'language','approved_by','approval_date','is_archived','career_stage','is_national','city']
        
    def clean(self):
        """
        يقوم بفحص ما إذا كانت المقالة موجودة بالفعل بنفس العنوان والتاريخ والمحتوى.
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
    extra=3,
    can_delete=True
)
        

    
