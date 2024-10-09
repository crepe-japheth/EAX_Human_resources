# Generated by Django 4.2.7 on 2024-10-07 12:47

from django.conf import settings
import django.contrib.auth.models
import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('first_login', models.BooleanField(default=True)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Department',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('department_name', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone_number', models.CharField(max_length=15)),
                ('sex', models.CharField(blank=True, choices=[('male', 'Male'), ('female', 'Female')], max_length=7, null=True)),
                ('salary', models.IntegerField()),
                ('position', models.CharField(max_length=200)),
                ('hire_date', models.DateField(blank=True, null=True)),
                ('date_of_birth', models.DateField(null=True)),
                ('rssb_id', models.CharField(max_length=200, null=True)),
                ('allowed_leave', models.IntegerField(blank=True, default=18, null=True)),
                ('taken_leave', models.IntegerField(blank=True, default=0, null=True)),
                ('initial_leave', models.IntegerField(blank=True, default=18, null=True)),
                ('photo', models.ImageField(blank=True, null=True, upload_to='profile/')),
                ('department', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='in_department', to='employee_leave.department')),
                ('user', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='NextOfKeen',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('next_of_keen_first_name', models.CharField(max_length=100)),
                ('next_of_keen_last_name', models.CharField(max_length=100)),
                ('next_of_keen_phone_number', models.CharField(max_length=100)),
                ('employee', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='next_of_keens', to='employee_leave.employee')),
            ],
        ),
        migrations.CreateModel(
            name='Leave',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('leave_type', models.CharField(choices=[('paid_leave', 'Paid Leave'), ('sick_leave', 'Sick Leave'), ('marternity_leave', 'Marternity Leave'), ('parternity_leave', 'Parternity Leave'), ('sabbatical_leave', 'Sabbatical Leave')], max_length=30)),
                ('leave_date', models.DateField()),
                ('return_date', models.DateField()),
                ('status', models.CharField(blank=True, choices=[('pending', 'Pending'), ('cancelled', 'Cancelled'), ('approved', 'Approved')], default='pending', max_length=30, null=True)),
                ('comment', models.TextField(blank=True, null=True)),
                ('employee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='EmployeeAttachment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('attachment_name', models.CharField(max_length=200)),
                ('file', models.FileField(upload_to='attachment/')),
                ('employee', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='attachments', to='employee_leave.employee')),
            ],
        ),
        migrations.AddField(
            model_name='department',
            name='department_head',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='department_supervisor', to='employee_leave.employee'),
        ),
    ]
