from django.shortcuts import render , redirect ,get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth .decorators import login_required
from django.contrib import messages
from django.db import transaction
from .models import *
from .forms import *

# Create your views here.
def login_view(request):
    if request.method == "POST":
        form = LoginForm(request.POST) 
        
        if form.is_valid():
            # عند استخدام form.cleaned_data فإنك تستخدم البيانات التي قام النموذج بتنظيفها
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
        
            user = authenticate(request , username=username , password=password)
        
            if user is not None:
                login(request , user)
                return redirect("dashboard") 
            
            else:
                # 1. فشل المصادقة، نضيف الخطأ ونقوم بالإرجاع فورًا
                form.add_error(None , "اسم المستخدم أو كلمة المرور غير صحيحة.") 
                return render(request, "archives/login.html" , {'form': form}) 
                
            
    else:
        # 3. طلب GET، إنشاء نموذج فارغ
        form = LoginForm()
        
    # 4. طلب GET، عرض النموذج الفارغ
    return render(request, "archives/login.html" , {'form': form})


def logout_view(request):
    logout(request)
    return redirect("home")

def index(request):
    return render(request, 'archives/index.html')

@login_required(login_url='/login/') 
def dashboard(request):
    return render(request, 'archives/dashboard/dashboard.html')

@login_required(login_url='/login/') 
def create_article_type(request):

    articleType = ArticleType.objects.all()
    show_modal = False
    if (request.POST):
        add_form = ArticleTypeForm(request.POST)
        if (add_form.is_valid()):
            try:
                add_form.save()
                messages.success(request,'تم حفظ نوع المقال بنجاح')
                return redirect('create_article_type') 
            except Exception as e:
                messages.error(request, 'حدث خطأ في البيانات المدخلة. يرجى مراجعة الحقول') 
                # print(f"Detailed Error: {e}")
        else:
            show_modal = True
            #messages.error(request, 'البيانات المدخلة غير صحيحة. يرجى مراجعة الحقول.')
            context = {'form': add_form, 'article_types': articleType , 'show_modal': show_modal}
            return render(request, "archives/dashboard/create_article_type.html", context)            
        
    # معالجة طلب العرض (GET) 
    else:
        add_form = ArticleTypeForm()
        
        context = {'form': add_form, 'article_types': articleType}
        return render(request, "archives/dashboard/create_article_type.html", context)
    
    
@login_required(login_url='/login/')
def update_article_type(request, pk):
    # 1. جلب الكائن المحدد (إذا لم يوجد، سيظهر خطأ 404)
    article_type_instance = get_object_or_404(ArticleType, id=pk)
    
    if request.method == 'POST':
        # 2. في حالة POST: ربط البيانات الجديدة مع الكائن الموجود
        form = ArticleTypeForm(request.POST, instance=article_type_instance)
        
        if form.is_valid():
            try:
                # 3. الحفظ الآمن للتعديلات
                with transaction.atomic():
                    form.save()
                    
                messages.success(request, f'تم تعديل نوع المقال "{article_type_instance.arabic_name}" بنجاح.')
                
                # العودة إلى صفحة القائمة الرئيسية (حيث تعرض جميع الأنواع)
                return redirect('create_article_type')
                
            except Exception as e:
                # 4. معالجة أخطاء الحفظ (مثل القيد الفريد أو أخطاء قاعدة البيانات)
                messages.error(request, 'حدث خطأ أثناء التعديل. يرجى مراجعة البيانات.')
                # عند الفشل، يستمر الكود لعرض النموذج مع رسالة الخطأ
                
        # إذا فشل التحقق (Validation)، يستمر الكود لعرض النموذج مع أخطاء التحقق
        
    else:
        # 5. في حالة GET: عرض النموذج محمل بالبيانات الحالية
        form = ArticleTypeForm(instance=article_type_instance)
        
    context = {
        'form': form,
        'instance': article_type_instance, # نرسل الكائن للعنوان أو معلومات أخرى
    }
    # نستخدم نفس قالب إنشاء النوع في الغالب، أو قالب مخصص للتعديل
    return render(request, "archives/dashboard/update_article_type.html", context)
