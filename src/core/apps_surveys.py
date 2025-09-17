from django.apps import AppConfig

class DjfSurveysConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'djf_surveys'        # path original de la app
    verbose_name = 'Encuestas'  # nombre para mostrar en el admin
