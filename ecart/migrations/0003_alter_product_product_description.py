# Generated by Django 3.2.4 on 2021-06-06 17:42

import ckeditor.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ecart', '0002_auto_20210606_1325'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='product_description',
            field=ckeditor.fields.RichTextField(),
        ),
    ]
