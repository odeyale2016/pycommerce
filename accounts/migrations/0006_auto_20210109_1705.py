# Generated by Django 3.1.5 on 2021-01-09 16:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_auto_20210109_1116'),
    ]

    operations = [
        migrations.RenameField(
            model_name='product',
            old_name='productname',
            new_name='name',
        ),
    ]
