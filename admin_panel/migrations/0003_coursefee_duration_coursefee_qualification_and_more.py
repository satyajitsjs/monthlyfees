# Generated by Django 4.1.6 on 2024-04-16 07:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('admin_panel', '0002_coursefee'),
    ]

    operations = [
        migrations.AddField(
            model_name='coursefee',
            name='duration',
            field=models.CharField(default='', max_length=50),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='coursefee',
            name='qualification',
            field=models.CharField(default='', max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='coursefee',
            name='subject',
            field=models.CharField(default='', max_length=100),
            preserve_default=False,
        ),
    ]
