# Generated by Django 4.2.6 on 2023-11-08 07:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employee_leave', '0002_alter_leave_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='employee',
            name='allowed_leave',
            field=models.IntegerField(blank=True, default=10, null=True),
        ),
    ]
