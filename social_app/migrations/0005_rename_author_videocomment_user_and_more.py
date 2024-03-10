# Generated by Django 5.0.1 on 2024-02-01 16:24

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('social_app', '0004_remove_uploadedvideo_comments'),
    ]

    operations = [
        migrations.RenameField(
            model_name='videocomment',
            old_name='author',
            new_name='user',
        ),
        migrations.AlterField(
            model_name='videocomment',
            name='text',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='videocomment',
            name='video',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='social_app.uploadedvideo'),
        ),
    ]
