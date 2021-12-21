from django.contrib import admin

# Register your models here.
from practice_app.models import MuseumAPICSV


class MuseumAPICSVAdmin(admin.ModelAdmin):
    class Meta:
        verbose_name = 'MuseumAPICSV'
        verbose_name_plural = 'MuseumAPICSV'


admin.site.register(MuseumAPICSV, MuseumAPICSVAdmin)
