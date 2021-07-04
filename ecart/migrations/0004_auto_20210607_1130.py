# Generated by Django 3.2.4 on 2021-06-07 06:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ecart', '0003_alter_product_product_description'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.AddField(
            model_name='product',
            name='color',
            field=models.CharField(choices=[(1, 'White'), (2, 'Black'), (3, 'Gold'), (4, 'Royal'), (5, 'Navy'), (6, 'Maroon'), (7, 'Purple'), (8, 'Brown'), (9, 'Lime'), (10, 'Silver')], default='', max_length=2),
        ),
        migrations.AddField(
            model_name='product',
            name='size',
            field=models.CharField(choices=[(1, 'XS'), (2, 'S'), (3, 'M'), (4, 'L'), (5, 'XL'), (6, 'XXL')], default='', max_length=1),
        ),
    ]
