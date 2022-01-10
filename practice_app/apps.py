from django.apps import AppConfig


class PracticeAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'practice_app'

    def ready(self):
        import practice_app.signals
