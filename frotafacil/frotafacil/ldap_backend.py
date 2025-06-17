from django.contrib.auth.models import User
from django.contrib.auth.backends import BaseBackend
from .ldap_auth import autenticar_usuario_ad

class ActiveDirectoryBackend(BaseBackend):
    def authenticate(self, request, username=None, password=None):
        resultado = autenticar_usuario_ad(username, password)
        if isinstance(resultado, dict):
            user, _ = User.objects.get_or_create(username=resultado['username'])
            if request is not None:
                request.session['nome_completo_ad'] = resultado['nome_completo']
            return user
        return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None