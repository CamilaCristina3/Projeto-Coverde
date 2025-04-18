# apps/loja/apps.py
from django.apps import AppConfig

class LojaConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.loja'  # Caminho completo
    verbose_name = 'Loja'