from datetime import timedelta
from django.utils import timezone
from apscheduler.schedulers.background import BackgroundScheduler

from apps.parts.models import AutoParts


def start():
    """
    This function is used to start the scheduler.
    """
    scheduler = BackgroundScheduler()
    scheduler.add_job(remove_new_flag_from_autoparts, "interval", hours=6)
    scheduler.start()


def remove_new_flag_from_autoparts():
    """
    This function is used to remove new flag from all auto parts.
    """
    AutoParts.objects.filter(
        is_new=True, date_of_pubication__lte=timezone.now() - timedelta(days=3)
    ).update(is_new=False)
