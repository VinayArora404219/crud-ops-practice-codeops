from django.db.models.signals import post_save
from django.dispatch import receiver

from practice_app.models import MuseumAPICSV


@receiver(post_save, sender=MuseumAPICSV)
def update_csv_data(sender, instance, **kwargs):
    print(instance.accessionNumber)
