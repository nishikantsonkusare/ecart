# Generated by Django 3.2.4 on 2021-06-08 08:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ecart', '0009_auto_20210608_1324'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='mrp',
            field=models.DecimalField(decimal_places=2, max_digits=10),
        ),
        migrations.AlterField(
            model_name='product',
            name='selling_price',
            field=models.DecimalField(decimal_places=2, max_digits=10),
        ),
    ]