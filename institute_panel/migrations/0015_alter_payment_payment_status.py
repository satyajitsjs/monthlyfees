# Generated by Django 4.1.6 on 2024-04-20 06:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('institute_panel', '0014_payment_order_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='payment',
            name='payment_status',
            field=models.IntegerField(choices=[(1, 'Payment Success')], default=1),
        ),
    ]
