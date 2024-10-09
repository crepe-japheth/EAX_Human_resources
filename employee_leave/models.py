from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser
from django.conf import settings


class CustomUser(AbstractUser):
    first_login = models.BooleanField(default=True)

    def __str__(self):
        return self.username

LEAVE_TYPE = (
    ('paid_leave', 'Paid Leave'),
    ('sick_leave', 'Sick Leave'),
    ('marternity_leave', 'Marternity Leave'),
    ('parternity_leave', 'Parternity Leave'),
    ('sabbatical_leave', 'Sabbatical Leave'),
)

STATUS = (
    ('pending', 'Pending'),
    ('cancelled', 'Cancelled'),
    ('approved', 'Approved'),
)

SUPERVISOR_STATUS = (
    ('pending', 'Pending'),
    ('cancelled', 'Cancelled'),
    ('approved', 'Approved'),
)



GENDER = (
    ('male', 'Male'),
    ('female', 'Female'),
)

class EmployeeAttachment(models.Model):
    employee = models.ForeignKey('Employee', on_delete=models.CASCADE, related_name='attachments', null=True, blank=False)
    attachment_name = models.CharField(max_length=200)
    file = models.FileField(upload_to='attachment/')


class Department(models.Model):
    department_name = models.CharField(max_length=200)
    department_head = models.OneToOneField("Employee",on_delete=models.SET_NULL, related_name="department_supervisor",null=True, blank=True)

    def __str__(self):
        return str(self.department_name)
    
    

class Employee(models.Model):
    first_name = models.CharField(max_length=200, null=True, blank=False)
    last_name = models.CharField(max_length=200, null=True, blank=False)
    email = models.EmailField(null=True, blank=False)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True)
    phone_number = models.CharField(max_length=15)
    sex = models.CharField(max_length=7,choices=GENDER, blank=True, null=True)
    salary = models.IntegerField()
    position = models.CharField(max_length=200)
    hire_date = models.DateField(null=True, blank=True)
    date_of_birth = models.DateField(null=True, blank=False)
    department = models.ForeignKey(Department,on_delete=models.SET_NULL, related_name="in_department",null=True, blank=False)
    rssb_id = models.CharField(max_length=200, null=True, blank=False)
    allowed_leave = models.IntegerField(default=18, blank=True, null=True)
    taken_leave = models.IntegerField(default=0, blank=True, null=True)
    initial_leave = models.IntegerField(default=18, blank=True, null=True)
    photo = models.ImageField(upload_to='profile/',blank=True, null=True)

    def __str__(self):
        return str(self.first_name)

class NextOfKeen(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='next_of_keens', null=True)
    next_of_keen_first_name = models.CharField(max_length=100)
    next_of_keen_last_name = models.CharField(max_length=100)
    next_of_keen_phone_number = models.CharField(max_length=100)

class Leave(models.Model):
    employee = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    leave_type = models.CharField(max_length=30, choices=LEAVE_TYPE)
    leave_date = models.DateField()
    return_date = models.DateField()
    status = models.CharField(max_length=30, choices=STATUS, default='pending', blank=True, null=True)
    supervisor_status = models.CharField(max_length=30, choices=SUPERVISOR_STATUS, default='pending', blank=True, null=True)
    comment = models.TextField(blank=True, null=True)
    

    def __str__(self):
        return f'{self.employee} - {self.leave_date}'







        