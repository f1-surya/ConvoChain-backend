# Generated by Django 4.1.4 on 2023-01-22 14:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tweets', '0011_delete_comment'),
    ]

    operations = [
        migrations.RenameField(
            model_name='tweet',
            old_name='tweet',
            new_name='body',
        ),
    ]
