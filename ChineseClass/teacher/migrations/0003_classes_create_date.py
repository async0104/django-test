# Generated by Django 3.0 on 2020-01-02 11:31

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('teacher', '0002_classes'),
    ]

    operations = [
        migrations.AddField(
            model_name='classes',
            name='create_date',
            field=models.DateField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
