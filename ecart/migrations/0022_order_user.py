# Generated by Django 3.2.4 on 2021-06-16 14:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ecart', '0021_order_price'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='user',
            field=models.CharField(default='', max_length=256),
        ),
    ]
