# Generated by Django 4.0 on 2021-12-21 10:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('practice_app', '0002_alter_museumapicsv_accessionnumber'),
    ]

    operations = [
        migrations.AlterField(
            model_name='museumapicsv',
            name='artistBeginDate',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='museumapicsv',
            name='artistEndDate',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
