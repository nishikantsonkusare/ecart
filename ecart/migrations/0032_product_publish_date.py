# Generated by Django 3.2.4 on 2021-07-04 14:48

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('ecart', '0031_banner'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='publish_date',
            field=models.DateField(default=django.utils.timezone.now),
        ),
    ]
