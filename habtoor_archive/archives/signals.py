# archives/signals.py

from django.db.models.signals import pre_delete , pre_save
from django.dispatch import receiver
from django.contrib.contenttypes.models import ContentType

from .models import Attachment, Article 


@receiver(pre_delete, sender=Article)
def delete_related_attachments(sender, instance, **kwargs):
    """
    يقوم بحذف جميع المرفقات المرتبطة بكائن Article قبل حذفه.
    """
    try:
        # 1. الحصول على ContentType للكائن المحذوف (Article)
        article_content_type = ContentType.objects.get_for_model(instance)
        
        # 2. تصفية المرفقات المرتبطة بهذا الكائن تحديداً
        attachments_to_delete = Attachment.objects.filter(
            content_type=article_content_type, 
            object_id=instance.pk
        )
        
        # 3. تنفيذ عملية الحذف
        count, _ = attachments_to_delete.delete()
        print(f"Deleted {count} attachments for Article ID: {instance.pk}")
        
    except Exception as e:
        # إذا حدث أي خطأ (مثل عدم وجود ContentType)، لا نمنع الحذف
        print(f"Error during attachment cleanup for Article {instance.pk}: {e}")

@receiver(pre_save, sender=Attachment)
def prevent_original_name_override(sender, instance, **kwargs):
    """
    تمنع تغيير original_name إذا كان الكائن موجوداً ولا يتم رفع ملف جديد.
    """
    # 1. إذا كان الكائن موجوداً بالفعل في قاعدة البيانات (تعديل وليس إضافة)
    if instance.pk:
        try:
            # 2. استرجاع النسخة القديمة من قاعدة البيانات
            old_instance = Attachment.objects.get(pk=instance.pk)
            
            # 3. مقارنة: إذا لم يتغير حقل 'file' في النسخة الجديدة
            # (أي أن المسار الحالي للملف هو نفس المسار القديم، ولا يوجد رفع جديد)
            # و الـ original_name في النسخة الحالية فارغ (في حالة تم مسحه لأي سبب)
            if old_instance.file == instance.file and not instance.original_name:
                 # 4. إعادة تعيين القيمة القديمة
                 instance.original_name = old_instance.original_name
            
            # 5. حالة التعديل على حقل آخر (مثلاً is_url) دون رفع ملف جديد
            # إذا لم يتم تغيير الملف، نضمن أن الاسم الأصلي لا يتغير أبدًا
            if 'file' not in instance._state.fields_cache and instance.file == old_instance.file:
                 instance.original_name = old_instance.original_name

        except Attachment.DoesNotExist:
            # هذا يحدث عند الإضافة الجديدة، لا نحتاج لفعل شيء
            pass