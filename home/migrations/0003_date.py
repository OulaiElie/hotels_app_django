# Generated by Django 3.1.2 on 2023-03-26 14:44

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0002_auto_20220518_1502'),
    ]

    operations = [
        migrations.CreateModel(
            name='Date',
            fields=[
                ('uid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateField(auto_now_add=True)),
                ('updated_at', models.DateField(auto_now_add=True)),
                ('start_date', models.DateField(verbose_name='YYYY-MM-DD')),
                ('end_date', models.DateField(verbose_name='YYYY-MM-DD')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
