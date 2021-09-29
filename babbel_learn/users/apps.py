from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class UsersConfig(AppConfig):
    name = "babbel_learn.users"
    verbose_name = _("Users")

    def ready(self):
        try:
            import babbel_learn.users.signals  # noqa F401
        except ImportError:
            pass
