from django.apps import AppConfig


class TaigaContribGitlabAuthAppConfig(AppConfig):
    name = "taiga_contrib_gitlab_auth"
    verbose_name = "Taiga contrib gitlab auth App Config"

    def ready(self):
        from taiga.auth.services import register_auth_plugin
        from . import services
        register_auth_plugin("gitlab", services.gitlab_login_func)

