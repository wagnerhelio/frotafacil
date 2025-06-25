from django_auth_adfs.backend import AdfsAuthCodeBackend
from .utils import get_adfs_settings
from django_auth_adfs.config import settings as adfs_settings

class DynamicAdfsAuthCodeBackend(AdfsAuthCodeBackend):
    def authenticate(self, request, **kwargs):
        adfs_config = get_adfs_settings()
        if adfs_config:
            for key, value in adfs_config.items():
                setattr(adfs_settings, key, value)
        return super().authenticate(request, **kwargs) 