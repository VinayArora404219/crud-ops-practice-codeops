# Generated by Django 4.0 on 2021-12-21 14:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('practice_app', '0007_alter_museumapicsv_gallerynumber'),
    ]

    operations = [
        migrations.AlterField(
            model_name='museumapicsv',
            name='constituentID',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]