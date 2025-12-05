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
def manage_article_type(request, pk=None):
    
    articleType = ArticleType.objects.all()
    show_modal = False
    instance = None # الكائن الذي سيتم تعديله
    
    # 1. تحديد وضع التعديل (Update)
    if pk:
        # إذا وجد PK، جلب الكائن أو إظهار خطأ 404
        instance = get_object_or_404(ArticleType, pk=pk) 
        
    
    if request.method == 'POST':
        # 2. في POST: يتم ربط البيانات المرسلة مع الكائن (instance=instance)
        add_form = ArticleTypeForm(request.POST, instance=instance)
        
        if add_form.is_valid():
            try:
                with transaction.atomic():
                    add_form.save()
                    
                # تحديد رسالة النجاح بناءً على العملية (إنشاء أو تعديل)
                action_text = "تم تعديل" if pk else "تم إنشاء"
                messages.success(request, f'{action_text} نوع المقال بنجاح.')
                return redirect('list_article_types') 
                
            except Exception as e:
                messages.error(request, 'حدث خطأ غير متوقع أثناء الحفظ. يرجى مراجعة البيانات.')
                show_modal = True # إبقاء النافذة مفتوحة عند فشل الحفظ
                # لا يوجد هنا return، سنعرض القالب في نهاية الدالة
                #print(e)
        
        else:
            # 3. في حالة فشل التحقق (Validation Error)
            show_modal = True
            # لا نستخدم messages.error هنا لأن الأخطاء تظهر مباشرة في حقول النموذج
            # لا يوجد هنا return، سنعرض القالب في نهاية الدالة

    else:
        # 4. طلب GET:
        #   - إذا كان هناك PK: يتم تحميل الفورم ببيانات الكائن instance
        #   - إذا لم يكن هناك PK: يتم تحميل فورم فارغ للإنشاء
        add_form = ArticleTypeForm(instance=instance)
        
        # 🚨 إذا كان تعديلاً (GET مع PK)، نفتح المودل تلقائياً
        if pk:
            show_modal = True
    
    # 5. نقطة العودة الموحدة
    context = {
        'form': add_form, 
        'article_types': articleType,
        'show_modal': show_modal,
        # يمكن إضافة المتغير instance لمساعدة القالب على معرفة وضع التعديل
        'instance': instance 
    }
    # 🚨 يجب استخدام قالب موحد للصفحة (مثلاً: article_type_list.html)
    return render(request, "archives/dashboard/article_type_list.html", context)

from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import transaction

# ... (استيراد ArticleType)

@login_required(login_url='/login/')
def delete_article_type(request, pk):
    article_type_instance = get_object_or_404(ArticleType, pk=pk)
    
    # 2. التأكد من أن الطلب هو POST للحذف الآمن (مهم جداً)
    # لا ينبغي أبداً السماح بالحذف عبر طلب GET
    if request.method == 'POST':
        try:
            name = article_type_instance.name_ar # لحفظ الاسم قبل الحذف للرسالة
            
            # 3. حذف الكائن
            with transaction.atomic():
                article_type_instance.delete()
                
            messages.success(request, f'تم حذف نوع المقال "{name}" بنجاح.')
            
        except Exception as e:
            messages.error(request, 'حدث خطأ أثناء محاولة الحذف. يرجى التأكد من عدم ارتباطه بعناصر أخرى.')
            
    return redirect('list_article_types')
    
    
   