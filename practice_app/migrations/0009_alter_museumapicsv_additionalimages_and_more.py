# Generated by Django 4.0 on 2021-12-22 03:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('practice_app', '0008_alter_museumapicsv_constituentid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='museumapicsv',
            name='additionalImages',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='museumapicsv',
            name='primaryImage',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='museumapicsv',
            name='primaryImageSmall',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
