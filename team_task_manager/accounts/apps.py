from django.apps import AppConfig


class AccountsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'team_task_manager.accounts'

    def ready(self):
        import team_task_manager.accounts.signals