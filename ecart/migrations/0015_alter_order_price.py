# Generated by Django 3.2.4 on 2021-06-16 12:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ecart', '0014_alter_order_price'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='price',
            field=models.IntegerField(),
        ),
    ]
