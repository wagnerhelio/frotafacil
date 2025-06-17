import os
import django
from django.contrib.auth import get_user_model
from dotenv import load_dotenv

# Carrega variáveis do .env
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '..', '.env'))

# Configura o ambiente do Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "memora.settings")
django.setup()

User = get_user_model()

username = os.getenv("DJANGO_SUPERUSER_USERNAME")
email = os.getenv("DJANGO_SUPERUSER_EMAIL")
password = os.getenv("DJANGO_SUPERUSER_PASSWORD")

if not User.objects.filter(username=username).exists():
    User.objects.create_superuser(
        username=username,
        email=email,
        password=password
    )
    print(f"✔️ Superusuário '{username}' criado com sucesso.")
else:
    print(f"⚠️ Superusuário '{username}' já existe. Nenhuma ação executada.")
