import os
import sys
import platform
import django
from pathlib import Path
from django.conf import settings

def print_header(title):
    print(f"\n{'='*40}")
    print(f"{title.upper():^40}")
    print(f"{'='*40}")

def check_python_environment():
    print_header("ambiente python")
    print(f"Python versão: {platform.python_version()}")
    print(f"Sistema operacional: {platform.system()} {platform.release()}")
    print(f"Path do interpretador: {sys.executable}")
    print(f"Encoding padrão: {sys.getdefaultencoding()}")

def check_django_environment():
    print_header("ambiente django")
    print(f"Django versão: {django.get_version()}")
    print(f"Debug mode: {'LIGADO' if settings.DEBUG else 'DESLIGADO'}")
    print(f"Allowed hosts: {settings.ALLOWED_HOSTS}")
    print(f"Banco de dados: {settings.DATABASES['default']['ENGINE']}")

def check_watchman_config():
    print_header("configuração watchman")
    try:
        import pywatchman
        watchman_version = pywatchman.__version__
        print(f"pywatchman versão: {watchman_version}")
    except ImportError:
        print("pywatchman: NÃO INSTALADO")
        return

    try:
        import subprocess
        watchman_cli = subprocess.check_output(['watchman', '--version']).decode().strip()
        print(f"Watchman CLI: {watchman_cli}")
    except Exception as e:
        print(f"Watchman CLI: NÃO DISPONÍVEL ({str(e)})")

    print(f"Watchman ativado: {'SIM' if os.getenv('DJANGO_WATCHMAN_RELOADER') == '1' else 'NÃO'}")

def check_installed_apps():
    print_header("aplicações instaladas")
    required_apps = ['crispy_forms', 'crispy_bootstrap5']
    for app in required_apps:
        status = "OK" if app in settings.INSTALLED_APPS else "FALTANDO"
        print(f"{app}: {status}")

def check_dependencies():
    print_header("dependências python")
    dependencies = {
        'django-crispy-forms': 'crispy_forms',
        'crispy-bootstrap5': 'crispy_bootstrap5',
        'pywatchman': 'pywatchman',
        'channels': 'channels'
    }
    
    for pkg, mod in dependencies.items():
        try:
            __import__(mod)
            version = sys.modules[mod].__version__
            print(f"{pkg}: {version}")
        except ImportError:
            print(f"{pkg}: NÃO INSTALADO")

def check_paths():
    print_header("caminhos importantes")
    base_dir = Path(__file__).resolve().parent.parent
    paths = {
        'Diretório base': base_dir,
        'Static files': settings.STATIC_ROOT or settings.STATICFILES_DIRS[0],
        'Media files': settings.MEDIA_ROOT,
        'Templates': settings.TEMPLATES[0]['DIRS'][0] if settings.TEMPLATES[0]['DIRS'] else 'Não configurado'
    }
    
    for name, path in paths.items():
        exists = "EXISTE" if Path(path).exists() else "NÃO EXISTE"
        print(f"{name}: {path} ({exists})")

def main():
    # Configura o ambiente Django
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'COVERDE.settings')
    django.setup()
    
    # Executa todas as verificações
    check_python_environment()
    check_django_environment()
    check_watchman_config()
    check_installed_apps()
    check_dependencies()
    check_paths()
    
    print_header("verificação concluída")

if __name__ == "__main__":
    main()