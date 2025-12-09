from django.shortcuts import render , redirect ,get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth .decorators import login_required
from django.contrib import messages
from django.db import transaction
from .models import *
from .forms import AuthorityForm , ArticleForm , CareerStageForm , ArticleTypeForm , AttachmentFormSet , LoginForm , AttachmentForm
from django.core.paginator import Paginator
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView , DetailView
from django.contrib.contenttypes.models import ContentType
from django.views.generic import DetailView
from django.db.models import ForeignKey, TextField


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
    """
    Mixin لإضافة منطق التعامل مع المرفقات العامة (Generic Formset)
    """
    attachment_formset_class = None  # سيتم تعيينه في الـ Views التي ترث منه

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if self.attachment_formset_class and 'attachment_formset' not in context:
            instance = self.object if hasattr(self, 'object') else None

            context['attachment_formset'] = self.attachment_formset_class(
                self.request.POST or None,
                self.request.FILES or None,
                instance=instance,
                prefix='attachments'
            )
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        attachment_formset = context['attachment_formset']

        try:
            with transaction.atomic():

                # 1) حفظ النموذج الأساسي
                self.object = form.save()

                # 2) حفظ المرفقات
                if attachment_formset.is_valid():
                    attachment_formset.instance = self.object

                    for attachment_form in attachment_formset.forms:
                        if attachment_form.has_changed() or attachment_form.cleaned_data.get('DELETE'):
                            
                            #  المنطق الصحيح: لا تعين original_name إلا إذا تم رفع ملف 
                            if attachment_form.cleaned_data.get('file'):
                                # إذا كان هناك ملف جديد مرفوع: نستخدم اسمه الجديد
                                attachment_form.instance.original_name = attachment_form.cleaned_data['file'].name
                            
                            # ⚠️ ملاحظة مهمة: 
                            # إذا لم يكن هناك ملف جديد مرفوع (أي: قمت بتعديل حقل can_be_shared فقط)،
                            # فإن original_name سيحتفظ بقيمته القديمة المخزنة في attachment_form.instance
                            # (أي القيمة المحملة من قاعدة البيانات)، ولن يتم تغييرها في هذه الخطوة.
                            
                            # تعيين created_by للمستخدم الحالي في المرفقات الجديدة فقط
                            if attachment_form.instance.pk is None and attachment_form.cleaned_data.get('file'):
                                attachment_form.instance.created_by = self.request.user

                    attachment_formset.save()

                else:
                    # عرض الأخطاء الحقيقية للـ formset
                    for form_err in attachment_formset.forms:
                        for field, errors in form_err.errors.items():
                            for error in errors:
                                messages.error(self.request, f"[Attachment] {field}: {error}")

                    return self.form_invalid(form)

                messages.success(self.request, f'تم حفظ {self.model._meta.verbose_name} بنجاح.')
                return redirect(self.get_success_url())

        except Exception as e:
            # عرض استثناء النظام الحقيقي
            messages.error(self.request, f"System Error: {str(e)}")
            return self.form_invalid(form)

    def form_invalid(self, form):
        # عرض الأخطاء الحقيقية للـ Form الأساسي
        for field, errors in form.errors.items():
            for error in errors:
                messages.error(self.request, f"[Main Form] {field}: {error}")

        return self.render_to_response(self.get_context_data(form=form))


class BaseDetailView(DetailView):
    """
    كلاس أساسي عام (Generic) لعرض تفاصيل أي كائن موديل.
    يقوم بجمع بيانات الحقول وتنسيقها بشكل آمن لتمريرها إلى القالب.
    """
    template_name = 'generic/detail.html' # اسم القالب الموحد
    context_object_name = 'item' 
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        current_object = self.object # الكائن (الموديل) الذي يتم عرضه
        
        if self.model and current_object:
            # تمرير أسماء الموديل للقالب (للاستخدام في العناوين والروابط)
            context['model_name'] = self.model._meta.model_name
            context['model_name_singular'] = self.model._meta.verbose_name
            
            # 🚨🚨 تجهيز بيانات الحقول (fields_data) 🚨🚨
            fields_data = []
            
            # المرور على جميع حقول الموديل
            for field in self.model._meta.fields:
                
                # تجاهل الحقول الداخلية وعلاقات Generic (إذا كانت غير مطلوبة للعرض التفصيلي)
                if field.name in ['id', 'content_type', 'object_id']:
                    continue

                # 💡 الحل لخطأ NameError: تهيئة المتغير قبل أي محاولة استخدام
                display_value = "—" # القيمة الافتراضية في حالة الفشل أو عدم وجود بيانات
                
                # محاولة الحصول على القيمة
                try:
                    value = getattr(current_object, field.name)
                    display_value = value
                    
                    # 1. معالجة حقول العلاقات (ForeignKey)
                    if field.is_relation and value is not None:
                        # عرض القيمة النصية للكائن المرتبط (باستخدام __str__)
                        display_value = str(value)
                    
                    # 2. معالجة الحقول النصية الكبيرة (TextField) للاقتصاص
                    elif isinstance(field, TextField) and display_value:
                        # اقتصاص النص الطويل للعرض
                        display_value = str(display_value) # التأكد من أنه نص
                        display_value = display_value[:200] + ('...' if len(display_value) > 200 else '')
                    
                    # 3. معالجة القيم الفارغة أو الخاطئة
                    elif display_value is None or display_value is False or display_value == "":
                         display_value = "—"
                         
                    # 4. معالجة حقول التاريخ والوقت (إذا لزم الأمر تنسيق محدد)
                    # يمكنك إضافة منطق لتنسيق التاريخ هنا:
                    # elif field.get_internal_type() in ('DateField', 'DateTimeField') and display_value:
                    #     display_value = display_value.strftime("%Y-%m-%d")
                        
                except AttributeError:
                    # في حالة فشل جلب الحقل بالاسم المحدد
                    display_value = "— (خطأ في الحقل)" 

                # إضافة بيانات الحقل إلى القائمة fields_data
                fields_data.append({
                    'label': field.verbose_name,
                    'value': display_value
                })
                
            context['fields_data'] = fields_data # تمرير القائمة الآمنة والمنسقة
            
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
                # 🚨 جلب المرفقات المرتبطة 🚨
                # (يفترض وجود related_name='attachments' في GenericForeignKey في موديل Attachment)
                related_attachments = current_object.attachments.all()
            except AttributeError:
                # لا يوجد حقل GenericForeignKey يسمى 'attachments' في هذا الموديل.
                related_attachments = Attachment.objects.none()

            context['attachments'] = related_attachments
            
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
    
    
# المقالات مع المرفقات

    
class ArticleListView(BaseListView):
    model = Article
    # form_class = ArticleForm 
    context_object_name = 'objects_list'
    # حقول البحث (عنوان، محتوى، محافظة، تاريخ نشر)
    filter_fields = ['title_ar', 'content', 'city__name_ar', 'publish_date'] 
    success_url = reverse_lazy('article-list')
    
    # يجب عليك هنا تجاوز get_queryset لمعالجة البحث على حقول ForeignKey مثل city__name_ar
    # Note: البحث عن التاريخ (publish_date) يتطلب منطق خاص بالتاريخ/النطاق.


class ArticleCreateView(GenericAttachmentMixin, BaseCreateView):
    model = Article
    form_class = ArticleForm # نفترض تعريفها
    attachment_formset_class = AttachmentFormSet # Formset الذي تم تعريفه في forms.py
    template_name = 'generic/create_with_form.html' # قالب جديد لدمج النموذجين
    success_url = reverse_lazy('article-list')
    
    def form_valid(self, form):
        # يمكنك تعيين المستخدم هنا إذا كان مطلوباً
        form.instance.created_by = self.request.user
        # form.instance.approved_by = self.request.user # إذا كان المستخدم هو المصادق تلقائيًا
        return super().form_valid(form)


class ArticleUpdateView(GenericAttachmentMixin, BaseUpdateView):
    model = Article
    form_class = ArticleForm # نفترض تعريفها
    attachment_formset_class = AttachmentFormSet
    template_name = 'generic/update_with_form.html'
    success_url = reverse_lazy('article-list')


class ArticleDeleteView(BaseDeleteView):
    model = Article
    success_url = reverse_lazy('article-list')
    


class ArticleTypeDetailView(BaseDetailView):
    model = ArticleType
    # template_name='generic/detail.html' موروث

class CareerStageDetailView(BaseDetailView):
    model = CareerStage
  
    
class AuthorityDetailView(BaseDetailView):
    model = Authority
  
    
class ArticleDetailView(GenericDetailMixin):
    model = Article
    
  

    
    
    
   