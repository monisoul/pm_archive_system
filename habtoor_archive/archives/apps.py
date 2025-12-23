from django.apps import AppConfig


class ArchivesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'archives'
    
    def ready(self):
        #  هذا هو السطر الذي يربط ملف signals.py عند بدء تشغيل Django 
        import archives.signals
