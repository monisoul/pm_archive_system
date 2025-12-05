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
def create_article_type(request, id=None):

    # جلب جميع أنواع المقالات لعرضها في الجدول
    article_types = ArticleType.objects.all()

    # إذا كنا في وضع التعديل، نجلب السجل حسب الـ id
    instance = ArticleType.objects.filter(id=id).first() if id else None

    # المتغير المسؤول عن فتح المودال تلقائيًا
    show_modal = False

    if request.method == "POST":

        # تعبئة النموذج مع ربطه بالـ instance إذا كان تعديل
        add_form = ArticleTypeForm(request.POST, instance=instance)

        # إذا كان النموذج صالحًا
        if add_form.is_valid():
            try:
                # الحفظ في قاعدة البيانات
                add_form.save()

                # رسالة نجاح
                if instance:
                    messages.success(request, "تم تعديل نوع المقال بنجاح")
                else:
                    messages.success(request, "تم حفظ نوع المقال بنجاح")

                # بعد الحفظ نعيد التوجيه لمنع إعادة إرسال البيانات
                return redirect('create_article_type')

            except Exception as e:
                # في حالة وجود خطأ من قاعدة البيانات
                messages.error(request, 'حدث خطأ في البيانات المدخلة. يرجى مراجعة الحقول') 
                # print(f"Detailed Error: {e}")

        else:
            # إذا كان تعديل → افتح المودال
            if instance:
                show_modal = True
            # إذا كان إضافة → افتح المودال
            else:
                show_modal = True

            context = {
                'form': add_form,                # النموذج الذي يحتوي الأخطاء
                'article_types': article_types,  # لعرض السجلات
                'show_modal': show_modal,        # لفتح المودال تلقائيًا
                'is_edit': True if instance else False,   # وضع تعديل أو إضافة
                'edit_id': id                    # رقم السجل الجاري تعديله
            }

            return render(request, "archives/dashboard/create_article_type.html", context)

    else:

        # إذا كان هناك id → هذا يعني أننا نفتح صفحة التعديل
        if instance:
            add_form = ArticleTypeForm(instance=instance)
            show_modal = True   # فتح المودال تلقائيًا عند التعديل
        else:
            # حالة الإضافة
            add_form = ArticleTypeForm()

        context = {
            'form': add_form,
            'article_types': article_types,
            'show_modal': show_modal,        # لفتح المودال عند التعديل
            'is_edit': True if instance else False,
            'edit_id': id
        }

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

@login_required(login_url='/login/')
def delete_article_type(request, id):
    try:
        item = ArticleType.objects.get(id=id)
    except ArticleType.DoesNotExist:
        messages.error(request, "العنصر غير موجود.")
        return redirect('create_article_type')

    if request.method == "POST":
        item.delete()
        messages.success(request, "تم حذف نوع المقال بنجاح.")
        return redirect('create_article_type')

    messages.error(request, "طلب غير صالح.")
    return redirect('create_article_type')
