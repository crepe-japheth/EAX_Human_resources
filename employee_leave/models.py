from django.db import models
from django.contrib.auth.models import User


LEAVE_TYPE = (
    ('paid_sick', 'Paid sick'),
    ('unpaid_sick', 'Unpaid sick'),
    ('paid_annual', 'Paid annual leave'),
    ('unpaid_annual', 'Unpaid annual leave'),
    ('incidental', 'Incidental leave'),
    ('other', 'other'),
)

STATUS = (
    ('pending', 'Pending'),
    ('cancelled', 'Cancelled'),
    ('approved', 'Approved'),
)

class Employee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, blank=True, null=True)
    phone_number = models.CharField(max_length=15)
    sex = models.CharField(max_length=7, blank=True, null=True)
    salary = models.IntegerField()
    position = models.CharField(max_length=200)
    hire_date = models.DateField(auto_now_add=True)
    allowed_leave = models.IntegerField(default=10, blank=True, null=True)
    taken_leave = models.IntegerField(default=0, blank=True, null=True)
    photo = models.ImageField(upload_to='profile/',blank=True, null=True)

    def __str__(self):
        return str(self.user)


class Leave(models.Model):
    employee = models.ForeignKey(User, on_delete=models.CASCADE)
    leave_type = models.CharField(max_length=30, choices=LEAVE_TYPE)
    leave_date = models.DateField()
    return_date = models.DateField()
    status = models.CharField(max_length=30, choices=STATUS, default='pending', blank=True, null=True)
    comment = models.TextField(blank=True, null=True)
    

    def __str__(self):
        return f'{self.employee} - {self.leave_date}'







        