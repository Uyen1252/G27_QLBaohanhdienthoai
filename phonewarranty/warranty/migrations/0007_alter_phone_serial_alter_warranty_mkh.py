# Generated by Django 4.1.7 on 2023-04-21 19:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('warranty', '0006_alter_warranty_start_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='phone',
            name='serial',
            field=models.CharField(max_length=255, unique=True),
        ),
        migrations.AlterField(
            model_name='warranty',
            name='MKH',
            field=models.CharField(max_length=255, unique=True),
        ),
    ]