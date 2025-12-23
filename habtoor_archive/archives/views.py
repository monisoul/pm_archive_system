from django.shortcuts import render , redirect ,get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth .decorators import login_required
from django.contrib import messages
from django.db import transaction
from .models import *
from .forms import AuthorityForm , ArticleForm , CareerStageForm , ArticleTypeForm , AttachmentFormSet ,PublicationPlatformForm,PublicationFormSet, LoginForm , AttachmentForm , CategoryForm , AuthorityTypeForm , GeographicalLocationForm , PublicationPlatformTypeForm
from django.core.paginator import Paginator
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView , DetailView
from django.contrib.contenttypes.models import ContentType
from django.views.generic import DetailView
from django.db.models import ForeignKey, TextField , DateTimeField


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
    excluded_list_fields = ['name_en' , 'title_en', 'language' , 'is_archived' , 'keywords']
    
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
                
                # تطبيق شرط الاستثناء
                if field.name in self.excluded_list_fields:
                    continue
                
                display_fields.append(field)
            
            context['model_fields'] = display_fields
            
        return context
    
class BaseCreateView(CreateView):

    def get_success_url(self):
        if self.success_url:
            return self.success_url
        return reverse_lazy('dashboard') 
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        #  تمرير اسم النموذج (model_name) إلى السياق 
        context['model_name'] = self.model._meta.model_name.lower() # القيمة ستكون 'article'
        context['model_name_singular'] = self.model._meta.verbose_name
        return context
        
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
    
class GenericAttachmentMixin:
    attachment_formset_class = None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        instance = self.object if hasattr(self, 'object') else None

        if self.attachment_formset_class:
            context['attachment_formset'] = self.attachment_formset_class(
                self.request.POST if self.request.method == "POST" else None,
                self.request.FILES if self.request.method == "POST" else None,
                instance=instance,
                prefix='attachments'
            )
        return context


    

class GenericPublicationMixin:
    publication_formset_class = None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        instance = self.object if hasattr(self, 'object') else None

        if self.publication_formset_class:
            if self.request.method == "POST":
                context['publication_formset'] = self.publication_formset_class(
                    self.request.POST,
                    self.request.FILES,   # ✅ هذا هو السطر الحاسم
                    instance=instance,
                    prefix='publications'
                )
            else:
                context['publication_formset'] = self.publication_formset_class(
                    instance=instance,
                    prefix='publications'
                )

        return context





class GenericRelatedSaveMixin:

    def form_valid(self, form):
        context = self.get_context_data()
        attachment_formset = context.get('attachment_formset')
        publication_formset = context.get('publication_formset')

        with transaction.atomic():
            # إنشاء المقالة بدون حفظ مباشر
            self.object = form.save(commit=False)

            # تعيين المستخدم الحالي كمُنشئ المقالة
            self.object.created_by = self.request.user

            # حفظ المقالة بعد تعيين created_by
            self.object.save()

            # حفظ الفورم سيت إذا موجود
            if attachment_formset:
                attachment_formset.instance = self.object
                if attachment_formset.is_valid():
                    # تعيين created_by لكل مرفق قبل الحفظ
                    for attachment_form in attachment_formset:
                        if attachment_form.instance.pk is None:  # فقط العناصر الجديدة
                            attachment_form.instance.created_by = self.request.user
                    attachment_formset.save()

            if publication_formset:
                publication_formset.instance = self.object
                if publication_formset.is_valid():
                    # تعيين created_by لكل ببلكشن قبل الحفظ
                    for publication_form in publication_formset:
                        if publication_form.instance.pk is None:  # فقط العناصر الجديدة
                            publication_form.instance.created_by = self.request.user
                    publication_formset.save()

        return super().form_valid(form)

class BaseDetailView(DetailView):
    """
    كلاس أساسي عام (Generic) لعرض تفاصيل أي كائن موديل.
    يعرض:
    - الحقول العادية كما هي
    - العلاقات (FK) بالاسم فقط
    - علاقات المستوى الثاني حسب تعريف الموديل (DETAIL_RELATIONS)
    """
    template_name = 'generic/detail.html'
    context_object_name = 'item'

    # --------------------------------------------------
    # 1) جلب خريطة العلاقات من الموديل إن وجدت
    # --------------------------------------------------
    def get_detail_relations(self, model):
        """
        مثال داخل الموديل:
        DETAIL_RELATIONS = {
            'Authority': ['type', 'location']
        }
        """
        return getattr(model, 'DETAIL_RELATIONS', {})

    # --------------------------------------------------
    # 2) عرض اسم علاقة مباشرة (FK)
    # --------------------------------------------------
    def render_fk_name(self, obj, field_name):
        related = getattr(obj, field_name, None)
        return str(related) if related else "—"

    # --------------------------------------------------
    # 3) عرض علاقات المستوى الثاني (اسم فقط)
    # --------------------------------------------------
    def render_nested_relations(self, obj, parent_field):
        results = []

        relations_map = self.get_detail_relations(obj.__class__)
        nested_fields = relations_map.get(parent_field, [])

        parent_obj = getattr(obj, parent_field, None)
        if not parent_obj:
            return results

        for nested_field in nested_fields:
            nested_obj = getattr(parent_obj, nested_field, None)
            if nested_obj:
                field = parent_obj._meta.get_field(nested_field)
                results.append({
                    'label': field.verbose_name,
                    'value': str(nested_obj)
                })

        return results

    # --------------------------------------------------
    # 4) بناء بيانات العرض النهائية
    # --------------------------------------------------
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        current_object = self.object

        # لتجنب NoReverseMatch
        context['model_name'] = self.model._meta.model_name if self.model else ''
        context['model_name_singular'] = self.model._meta.verbose_name

        fields_data = []

        for field in self.model._meta.fields:

            # استثناء الحقول الإدارية
            if field.name in ['id', 'created_at', 'updated_at', 'content_type', 'object_id']:
                continue

            # ---------- ForeignKey ----------
            if isinstance(field, models.ForeignKey):
                # العلاقة الأساسية
                fields_data.append({
                    'label': field.verbose_name,
                    'value': self.render_fk_name(current_object, field.name)
                })

                # علاقات المستوى الثاني
                fields_data.extend(
                    self.render_nested_relations(current_object, field.name)
                )

            # ---------- TextField ----------
            elif isinstance(field, TextField):
                value = getattr(current_object, field.name, None)
                if value:
                    value = str(value)
                    value = value[:200] + ('...' if len(value) > 200 else value)
                else:
                    value = "—"

                fields_data.append({
                    'label': field.verbose_name,
                    'value': value
                })

            # ---------- حقل عادي ----------
            else:
                value = getattr(current_object, field.name, None)
                fields_data.append({
                    'label': field.verbose_name,
                    'value': value if value not in [None, ""] else "—"
                })

        context['fields_data'] = fields_data
        return context

    
class GenericDetailMixin(BaseDetailView):
    """
    Mixin/View لـ Detail View، يقوم بجلب المرفقات بالإضافة إلى البيانات الأساسية.
    هذا الكلاس مخصص للجداول المرتبطة بالمرفقات (مثل Article).
    """
    
    # model و context_object_name موروثين من BaseDetailView
    
    def get_context_data(self, **kwargs):
        # 1. استدعاء التابع الأساسي (BaseDetailView) لجلب الكائن وبيانات الموديل
        context = super().get_context_data(**kwargs)
        
        current_object = self.object
        
        if current_object:
            try:
                #  جلب المرفقات المرتبطة 
                # (يفترض وجود related_name='attachments' في GenericForeignKey في موديل Attachment)
                related_attachments = current_object.attachments.all()
            except AttributeError:
                # لا يوجد حقل GenericForeignKey يسمى 'attachments' في هذا الموديل.
                related_attachments = Attachment.objects.none()

            context['attachments'] = related_attachments
            context['publications'] = getattr(self.object, 'publications', []).all()

            
        return context

# صفحة أنواع المقالات
class ArticleTypeListView(BaseListView):
    model = ArticleType
    form_class = ArticleTypeForm
    context_object_name = 'objects_list'
    #success_url = reverse_lazy('article-type-list')
    
class ArticleTypeCreateView(BaseCreateView):
    model = ArticleType
    form_class = ArticleTypeForm
    template_name = 'generic/create_with_form.html'
    success_url = reverse_lazy('articletype-list')   
    
    
class ArticleTypeUpdateView(BaseUpdateView):
    model = ArticleType
    form_class = ArticleTypeForm
    success_url = reverse_lazy('articletype-list')

class ArticleTypeDeleteView(BaseDeleteView):
    model = ArticleType
    success_url = reverse_lazy('articletype-list')
    
class ArticleTypeDetailView(BaseDetailView):
    model = ArticleType
    # template_name='generic/detail.html' موروث
    

# المراحل المهنية

class CareerStageListView(BaseListView):
    model = CareerStage
    form_class = CareerStageForm
    context_object_name = 'objects_list'
    success_url = reverse_lazy('careerstage-list')
    
class CareerStageCreateView(BaseCreateView):
    model = CareerStage
    form_class = CareerStageForm
    template_name = 'generic/create_with_form.html'
    success_url = reverse_lazy('careerstage-list')   
    
    
class CareerStageUpdateView(BaseUpdateView):
    model = CareerStage
    form_class = CareerStageForm
    success_url = reverse_lazy('careerstage-list')

class CareerStageDeleteView(BaseDeleteView):
    model = CareerStage
    success_url = reverse_lazy('careerstage-list')
    
class CareerStageDetailView(BaseDetailView):
    model = CareerStage
  
    
 
# الجهات
class AuthorityListView(BaseListView):
    model = Authority
    form_class = AuthorityForm
    context_object_name = 'objects_list'
    success_url = reverse_lazy('authority-list')
    
class AuthorityCreateView(BaseCreateView):
    model = Authority
    form_class = AuthorityForm
    template_name = 'generic/create_with_form.html'
    success_url = reverse_lazy('authority-list')   
    
    
class AuthorityUpdateView(BaseUpdateView):
    model = Authority
    form_class = AuthorityForm
    success_url = reverse_lazy('authority-list')

class AuthorityDeleteView(BaseDeleteView):
    model = Authority
    success_url = reverse_lazy('authority-list')

class AuthorityDetailView(BaseDetailView):
    model = Authority
  
    
    
# المقالات مع المرفقات
    
class ArticleListView(BaseListView):
    model = Article
    context_object_name = 'objects_list'
    filter_fields = ['title_ar', 'content', 'city__name_ar', 'publish_date'] 
    success_url = reverse_lazy('article-list')
    


class ArticleCreateView(
    LoginRequiredMixin,
    GenericAttachmentMixin,
    GenericPublicationMixin,
    GenericRelatedSaveMixin,
    BaseCreateView):
    
    model = Article
    form_class = ArticleForm  
    attachment_formset_class = AttachmentFormSet # Formset الذي تم تعريفه في forms.py
    publication_formset_class = PublicationFormSet
    template_name = 'generic/create_with_form.html' # قالب جديد لدمج النموذجين
    success_url = reverse_lazy('article-list')
    
    
      
    

class ArticleUpdateView(
    LoginRequiredMixin,
    GenericAttachmentMixin,
    GenericPublicationMixin,
    GenericRelatedSaveMixin,
    BaseUpdateView
    ):
    model = Article
    form_class = ArticleForm # نفترض تعريفها
    attachment_formset_class = AttachmentFormSet
    publication_formset_class = PublicationFormSet
    template_name = 'generic/update_with_form.html'
    success_url = reverse_lazy('article-list')


class ArticleDeleteView(BaseDeleteView):
    model = Article
    success_url = reverse_lazy('article-list')
    
    
class ArticleDetailView(GenericDetailMixin):
    model = Article
    
    
# التصنيفات
class CategoryListView(BaseListView):
    model = Category
    form_class = CategoryForm
    context_object_name = 'objects_list'
    #success_url = reverse_lazy('article-type-list')
    
class CategoryCreateView(BaseCreateView):
    model = Category
    form_class = CategoryForm
    template_name = 'generic/create_with_form.html'
    success_url = reverse_lazy('category-list')   
    
    
class CategoryUpdateView(BaseUpdateView):
    model = Category
    form_class = CategoryForm
    success_url = reverse_lazy('category-list')

class CategoryDeleteView(BaseDeleteView):
    model = Category
    success_url = reverse_lazy('category-list')
    
class CategoryDetailView(BaseDetailView):
    model = Category
    
    
# انواع الجهات
class AuthorityTypeListView(BaseListView):
    model = AuthorityType
    form_class = AuthorityTypeForm
    context_object_name = 'objects_list'
   
    
class AuthorityTypeCreateView(BaseCreateView):
    model = AuthorityType
    form_class = AuthorityTypeForm
    template_name = 'generic/create_with_form.html'
    success_url = reverse_lazy('authoritytype-list')   
    
    
class AuthorityTypeUpdateView(BaseUpdateView):
    model = AuthorityType
    form_class = AuthorityTypeForm
    success_url = reverse_lazy('authoritytype-list')

class AuthorityTypeDeleteView(BaseDeleteView):
    model = AuthorityType
    success_url = reverse_lazy('authoritytype-list')
    
class AuthorityTypeDetailView(BaseDetailView):
    model = AuthorityType
    

# المواقع الجغرافية
class GeographicalLocationListView(BaseListView):
    model = GeographicalLocation
    form_class = GeographicalLocationForm
    context_object_name = 'objects_list'
   
    
class GeographicalLocationCreateView(BaseCreateView):
    model = GeographicalLocation
    form_class = GeographicalLocationForm
    template_name = 'generic/create_with_form.html'
    success_url = reverse_lazy('geographicallocation-list')   
    
    
class GeographicalLocationUpdateView(BaseUpdateView):
    model = GeographicalLocation
    form_class = GeographicalLocationForm
    success_url = reverse_lazy('ageographicallocation-list')

class GeographicalLocationDeleteView(BaseDeleteView):
    model = GeographicalLocation
    success_url = reverse_lazy('geographicallocation-list')
    
class GeographicalLocationDetailView(BaseDetailView):
    model = GeographicalLocation
    
    
# انواع المنصات 

class PublicationPlatformTypeListView(BaseListView):
    model = PublicationPlatformType
    form_class = PublicationPlatformTypeForm
    context_object_name = 'objects_list'
   
    
class PublicationPlatformTypeCreateView(BaseCreateView):
    model = PublicationPlatformType
    form_class = PublicationPlatformTypeForm
    template_name = 'generic/create_with_form.html'
    success_url = reverse_lazy('publicationplatformtype-list')   
    
    
class PublicationPlatformTypeUpdateView(BaseUpdateView):
    model = PublicationPlatformType
    form_class = PublicationPlatformTypeForm
    success_url = reverse_lazy('publicationplatformtype-list')

class PublicationPlatformTypeDeleteView(BaseDeleteView):
    model = PublicationPlatformType
    success_url = reverse_lazy('publicationplatformtype-list')
    
class PublicationPlatformTypeDetailView(BaseDetailView):
    model = PublicationPlatformType
    
    
# المنصات
class PublicationPlatformListView(BaseListView):
    model = PublicationPlatform
    form_class = PublicationPlatformForm
    context_object_name = 'objects_list'
   
    
class PublicationPlatformCreateView(BaseCreateView):
    model = PublicationPlatform
    form_class = PublicationPlatformForm
    template_name = 'generic/create_with_form.html'
    success_url = reverse_lazy('publicationplatform-list')   
    
    
class PublicationPlatformUpdateView(BaseUpdateView):
    model = PublicationPlatform
    form_class = PublicationPlatformForm
    success_url = reverse_lazy('publicationplatform-list')

class PublicationPlatformDeleteView(BaseDeleteView):
    model = PublicationPlatform
    success_url = reverse_lazy('publicationplatform-list')
    
class PublicationPlatformDetailView(BaseDetailView):
    model = PublicationPlatform


    
    
  

    
  

    
    
    
    
    
    
   