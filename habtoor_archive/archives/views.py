from django.shortcuts import render , redirect ,get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth .decorators import login_required
from django.contrib import messages
from django.db import transaction
from .models import *
from .forms import *
from django.core.paginator import Paginator
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView


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

    
class BaseListView(ListView):
    template_name = 'generic/list_with_form.html'  # تمبلت واحد لكل الجداول
    #success_url = None  # سيتم تحديدها في subclasses
    paginate_by = 10
    filter_fields = ['name_ar']
    
    def get_queryset(self):
        queryset = super().get_queryset()
        
        # 1. استخدام اسم متغير البحث من القالب
        search_query = self.request.GET.get('search') 
        
        if search_query:
            from django.db.models import Q
            q_objects = Q()
            
            # بناء استعلام البحث
            for field in self.filter_fields:
                q_objects |= Q(**{f'{field}__icontains': search_query})
            
            queryset = queryset.filter(q_objects)
        
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        if hasattr(self, 'form_class'):
            if 'form' not in context:
                context['form'] = self.form_class() 
        
        if self.model:
            context['model_name_singular'] = self.model._meta.verbose_name
            context['model_name_plural'] = self.model._meta.verbose_name_plural
            
            
            context['model_name'] = self.model._meta.model_name
            
            
            display_fields = []
            for field in self.model._meta.fields:
                display_fields.append(field)
            
            context['model_fields'] = display_fields
            
        return context
    
class BaseCreateView(CreateView):

    def get_success_url(self):
        if self.success_url:
            return self.success_url
        return reverse_lazy('dashboard') 
        
    def form_valid(self, form):
        messages.success(self.request, f'تم إضافة {self.model._meta.verbose_name} بنجاح.')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'فشل في الإضافة. يرجى مراجعة الأخطاء.')
        
        return redirect(self.get_success_url())
    
class BaseUpdateView(UpdateView):
    template_name = 'generic/update_with_form.html'
    success_url = None
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        if self.model:
            context['model_name_singular'] = self.model._meta.verbose_name
            context['model_name_plural'] = self.model._meta.verbose_name_plural
            context['operation'] = 'Update' 
            
            context['model_name'] = self.model._meta.model_name
            
        return context
    
    def form_valid(self, form):
        messages.success(self.request, f'تم تعديل {self.model._meta.verbose_name} بنجاح.')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'فشل التعديل. يرجى مراجعة الأخطاء في النموذج.')
        return super().form_invalid(form)
    

class BaseDeleteView(DeleteView):
    template_name = 'generic/confirm_delete.html'
    success_url = None
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        if self.model:
            context['model_name_singular'] = self.model._meta.verbose_name
            context['model_name_plural'] = self.model._meta.verbose_name_plural
            context['model_name'] = self.model._meta.model_name
            
        return context
    
    def form_valid(self, form):
        name_of_object = self.object 
        model_name = self.model._meta.verbose_name
        
        try:
            display_name = getattr(name_of_object, 'name', str(name_of_object))
            messages.success(self.request, f'تم حذف {model_name} "{display_name}" بنجاح.')
        except Exception:
            messages.success(self.request, f'تم حذف {model_name} بنجاح.')
            
        return super().form_valid(form)
    
# صفحة أنواع المقالات
class ArticleTypeListView(BaseListView):
    model = ArticleType
    form_class = ArticleTypeForm
    context_object_name = 'objects_list'
    #success_url = reverse_lazy('article-type-list')
    
class ArticleTypeCreateView(BaseCreateView):
    model = ArticleType
    form_class = ArticleTypeForm
    success_url = reverse_lazy('dashboard')   
    
    
class ArticleTypeUpdateView(BaseUpdateView):
    model = ArticleType
    form_class = ArticleTypeForm
    success_url = reverse_lazy('articletype-list')

class ArticleTypeDeleteView(BaseDeleteView):
    model = ArticleType
    success_url = reverse_lazy('articletype-list')
    


class CareerStageListView(BaseListView):
    model = CareerStage
    form_class = CareerStageForm
    context_object_name = 'objects_list'
    success_url = reverse_lazy('careerstage-list')
    
class CareerStageCreateView(BaseCreateView):
    model = CareerStage
    form_class = CareerStageForm
    success_url = reverse_lazy('careerstage-list')   
    
    
class CareerStageUpdateView(BaseUpdateView):
    model = CareerStage
    form_class = CareerStageForm
    success_url = reverse_lazy('careerstage-list')

class CareerStageDeleteView(BaseDeleteView):
    model = CareerStage
    success_url = reverse_lazy('careerstage-list')
 
    




    
    
    
   