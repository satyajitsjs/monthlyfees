# Generated by Django 4.1.6 on 2024-04-15 09:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('admin_panel', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('admission_number', models.CharField(max_length=20, unique=True)),
                ('name', models.CharField(max_length=100)),
                ('student_class', models.CharField(max_length=20)),
                ('section', models.CharField(max_length=10)),
                ('course', models.CharField(choices=[('BSE', 'BSE'), ('CBSE', 'CBSE'), ('Competitive', 'Competitive')], max_length=20)),
                ('contact_number', models.CharField(max_length=15)),
                ('gender', models.CharField(max_length=10)),
                ('institute', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='admin_panel.institute')),
            ],
        ),
    ]
