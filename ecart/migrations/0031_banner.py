# Generated by Django 3.2.4 on 2021-07-01 16:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ecart', '0030_alter_product_thumbnail'),
    ]

    operations = [
        migrations.CreateModel(
            name='Banner',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(null=True, upload_to='banner/')),
            ],
        ),
    ]