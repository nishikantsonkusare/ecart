# Generated by Django 3.2.4 on 2021-06-27 07:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ecart', '0025_alter_order_order_amount'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='profile_image',
            field=models.ImageField(blank=True, default='', upload_to='profile/'),
        ),
    ]