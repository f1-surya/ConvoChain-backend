# Generated by Django 4.1.4 on 2023-01-11 09:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tweets', '0010_rename_posted_by_comment_author_and_more'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Comment',
        ),
    ]
