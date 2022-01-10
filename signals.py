from django.db.models.signals import post_save
from django.dispatch import receiver

from practice_app.models import MuseumAPICSV


@receiver(post_save, sender=MuseumAPICSV)
def csv_data_uploaded(sender, instance, created, **kwargs):
    if created:
        print(instance.objects.all())


@receiver(post_save, sender=MuseumAPICSV)
def csv_data_updated(sender, instance, **kwargs):
    print(instance)
    instance.profile.save()
