# Generated by Django 4.1.7 on 2023-04-21 19:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('warranty', '0003_phone_delete_customer_remove_warranty_serial_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='warranty',
            name='MKH',
            field=models.CharField(default=2, max_length=255),
            preserve_default=False,
        ),
    ]