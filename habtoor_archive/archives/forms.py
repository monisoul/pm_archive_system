from django import forms
from .models import *

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
        

    
