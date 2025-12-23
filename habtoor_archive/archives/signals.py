# archives/signals.py

from django.db.models.signals import pre_delete , pre_save , post_delete
from django.dispatch import receiver
from django.contrib.contenttypes.models import ContentType
from .models import Attachment, Article , Publication
import os

# حذف ملفات cover_image و page_image عند حذف Publication
# @receiver(post_delete, sender=Publication)
# def delete_publication_files(sender, instance, **kwargs):
#     if instance.cover_image:
#         instance.cover_image.delete(save=False)
#     if instance.page_image:
#         instance.page_image.delete(save=False)

# @receiver(post_delete, sender=Attachment)
# def delete_attachment_file(sender, instance, **kwargs):
#     """
#     حذف الملف الفيزيائي من media عند حذف المرفق من قاعدة البيانات
#     """
#     if instance.file:
#         try:
#             instance.file.delete(save=False)
#         except Exception as e:
#             print(f"Error deleting file {instance.file}: {e}")



# @receiver(pre_delete, sender=Article)
# def delete_related_attachments(sender, instance, **kwargs):
#     """
#     يقوم بحذف جميع المرفقات المرتبطة بكائن Article قبل حذفه.
#     """
#     try:
#         # 1. الحصول على ContentType للكائن المحذوف (Article)
#         article_content_type = ContentType.objects.get_for_model(instance)
        
#         # 2. تصفية المرفقات المرتبطة بهذا الكائن تحديداً
#         attachments_to_delete = Attachment.objects.filter(
#             content_type=article_content_type, 
#             object_id=instance.pk
#         )
        
#         # 3. تنفيذ عملية الحذف
#         count, _ = attachments_to_delete.delete()
#         print(f"Deleted {count} attachments for Article ID: {instance.pk}")
        
#     except Exception as e:
#         # إذا حدث أي خطأ (مثل عدم وجود ContentType)، لا نمنع الحذف
#         print(f"Error during attachment cleanup for Article {instance.pk}: {e}")

# @receiver(pre_save, sender=Attachment)
# def prevent_original_name_override(sender, instance, **kwargs):
#     """
#     تمنع تغيير original_name إذا كان الكائن موجوداً ولا يتم رفع ملف جديد.
#     """
#     # 1. إذا كان الكائن موجوداً بالفعل في قاعدة البيانات (تعديل وليس إضافة)
#     if instance.pk:
#         try:
#             # 2. استرجاع النسخة القديمة من قاعدة البيانات
#             old_instance = Attachment.objects.get(pk=instance.pk)
            
#             # 3. مقارنة: إذا لم يتغير حقل 'file' في النسخة الجديدة
#             # (أي أن المسار الحالي للملف هو نفس المسار القديم، ولا يوجد رفع جديد)
#             # و الـ original_name في النسخة الحالية فارغ (في حالة تم مسحه لأي سبب)
#             if old_instance.file == instance.file and not instance.original_name:
#                  # 4. إعادة تعيين القيمة القديمة
#                  instance.original_name = old_instance.original_name
            
#             # 5. حالة التعديل على حقل آخر (مثلاً is_url) دون رفع ملف جديد
#             # إذا لم يتم تغيير الملف، نضمن أن الاسم الأصلي لا يتغير أبدًا
#             if 'file' not in instance._state.fields_cache and instance.file == old_instance.file:
#                  instance.original_name = old_instance.original_name

#         except Attachment.DoesNotExist:
#             # هذا يحدث عند الإضافة الجديدة، لا نحتاج لفعل شيء
#             pass
        
# @receiver(pre_save, sender=Attachment)
# def delete_old_attachment_file_on_change(sender, instance, **kwargs):
#     """حذف ملف المرفق القديم عند التعديل"""  
#     if not instance.pk:
#         return  # إضافة جديدة

#     try:
#         old_instance = Attachment.objects.get(pk=instance.pk)
#     except Attachment.DoesNotExist:
#         return

#     if old_instance.file and old_instance.file != instance.file:
#         if os.path.isfile(old_instance.file.path):
#             old_instance.file.delete(save=False)
            
# @receiver(post_delete, sender=Attachment)
# def delete_attachment_file_on_delete(sender, instance, **kwargs):
#     """حذف ملف المرفق عند الحذف"""
#     if instance.file:
#         instance.file.delete(save=False)

            
# @receiver(pre_save, sender=Publication)
# def delete_old_publication_images_on_change(sender, instance, **kwargs):
#     """حذف صور Publication القديمة عند التعديل"""
#     if not instance.pk:
#         return

#     try:
#         old = Publication.objects.get(pk=instance.pk)
#     except Publication.DoesNotExist:
#         return

#     # صورة الصفحة
#     if old.page_image and old.page_image != instance.page_image:
#         old.page_image.delete(save=False)

#     # صورة الغلاف
#     if old.cover_image and old.cover_image != instance.cover_image:
#         old.cover_image.delete(save=False)
        
# @receiver(post_delete, sender=Publication)
# def delete_publication_images_on_delete(sender, instance, **kwargs):
#     """حذف صور Publication عند الحذف"""
#     if instance.page_image:
#         instance.page_image.delete(save=False)

#     if instance.cover_image:
#         instance.cover_image.delete(save=False)

@receiver(pre_save, sender=Attachment)
def delete_old_attachment_file_on_change(sender, instance, **kwargs):
    if not instance.pk:
        return

    try:
        old = Attachment.objects.get(pk=instance.pk)
    except Attachment.DoesNotExist:
        return

    if old.file and old.file != instance.file:
        if old.file.path and os.path.isfile(old.file.path):
            old.file.delete(save=False)


@receiver(post_delete, sender=Attachment)
def delete_attachment_file_on_delete(sender, instance, **kwargs):
    if instance.file and instance.file.path:
        if os.path.isfile(instance.file.path):
            instance.file.delete(save=False)


@receiver(pre_save, sender=Publication)
def delete_old_publication_images_on_change(sender, instance, **kwargs):
    if not instance.pk:
        return

    try:
        old = Publication.objects.get(pk=instance.pk)
    except Publication.DoesNotExist:
        return

    if old.page_image and old.page_image != instance.page_image:
        if os.path.isfile(old.page_image.path):
            old.page_image.delete(save=False)

    if old.cover_image and old.cover_image != instance.cover_image:
        if os.path.isfile(old.cover_image.path):
            old.cover_image.delete(save=False)


@receiver(post_delete, sender=Publication)
def delete_publication_images_on_delete(sender, instance, **kwargs):
    if instance.page_image and os.path.isfile(instance.page_image.path):
        instance.page_image.delete(save=False)

    if instance.cover_image and os.path.isfile(instance.cover_image.path):
        instance.cover_image.delete(save=False)



@receiver(post_delete, sender=Article)
def delete_article_attachments(sender, instance, **kwargs):
    content_type = ContentType.objects.get_for_model(Article)

    attachments = Attachment.objects.filter(
        content_type=content_type,
        object_id=instance.pk
    )

    for att in attachments:
        att.delete()

