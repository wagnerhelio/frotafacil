import os
import django
from django.contrib.auth import get_user_model

# Configura o ambiente do Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "frotafacil.settings")
django.setup()

User = get_user_model()

username = "admin"
email = "admin@admin.com"
password = "admin"

if not User.objects.filter(username=username).exists():
    User.objects.create_superuser(
        username=username,
        email=email,
        password=password
    )
    print(f"✔️ Superusuário '{username}' criado com sucesso.")
else:
    print(f"⚠️ Superusuário '{username}' já existe. Nenhuma ação executada.")
