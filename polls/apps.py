"""Poll app for django."""
from django.apps import AppConfig


class PollsConfig(AppConfig):
    """Polls config."""
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'polls'

    def ready(self):
        """Import signal to make it run after the app is run."""
        import polls.signals
