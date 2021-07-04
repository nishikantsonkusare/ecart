# Generated by Django 3.2.4 on 2021-06-06 07:44

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('product_name', models.CharField(max_length=100)),
                ('product_description', models.CharField(max_length=1000)),
                ('mrp', models.PositiveIntegerField()),
                ('selling_price', models.PositiveIntegerField()),
                ('stock', models.PositiveIntegerField()),
            ],
        ),
    ]