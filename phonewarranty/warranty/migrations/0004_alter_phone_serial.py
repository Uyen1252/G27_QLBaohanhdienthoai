# Generated by Django 4.2.1 on 2023-05-22 01:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('warranty', '0003_alter_phone_serial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='phone',
            name='serial',
            field=models.IntegerField(),
        ),
    ]
