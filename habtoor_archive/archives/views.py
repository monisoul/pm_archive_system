from django.shortcuts import render , redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth .decorators import login_required
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
    if (request.POST):
        add_form = ArticleTypeForm(request.POST)
        if (add_form.is_valid()):
            add_form.save()
            return redirect('home')
    else:
        add_form = ArticleTypeForm()
        
        return render(request, "archives/dashboard/create_article_type.html", {'form' : add_form , 'article_types' : articleType})   
    
