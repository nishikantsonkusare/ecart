# Generated by Django 3.2.4 on 2021-06-29 17:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ecart', '0029_auto_20210629_2259'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='thumbnail',
            field=models.ImageField(blank=True, default='', upload_to='product/'),
        ),
    ]