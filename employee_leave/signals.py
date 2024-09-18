from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from .send_email import send_mail_to_employee
from .models import Employee, CustomUser, Leave
from decouple import config
from .annual_leave_calc import calc_annual



@receiver(post_save, sender=Leave)
def leave_created_signal(sender, instance, created, **kwargs):
    if created:
        print("leave is being applied")
    else:
        if instance.status == 'approved':
            employee_obj = Employee.objects.filter(user=instance.employee)[0]
            employee_obj.allowed_leave = employee_obj.allowed_leave - calc_annual(str(instance.leave_date), str(instance.return_date))[1]
            employee_obj.taken_leave = employee_obj.taken_leave + calc_annual(str(instance.leave_date), str(instance.return_date))[1]
            employee_obj.save()


# @receiver(post_save, sender=Leave)
# def leave_created_signal(sender, instance, created, **kwargs):
#     if created:
#         try:
#             send_mail_to_employee(config("HR_EMAIL"), instance.leave_date, instance.return_date,instance.status, instance.employee.username, instance.leave_type)
#         except Exception as error:
#             print(error)
#             print(f'the leave is being applied {instance.employee.username} - {instance.leave_date}')
#     else:
#         if instance.status == 'approved':
#             employee = Employee.objects.filter(user=instance.employee)[0]
#             employee.taken_leave +=1
#             employee.save()
#         try:
#             send_mail_to_employee(instance.employee.email, instance.leave_date, instance.return_date,instance.status, instance.employee.username, instance.leave_type)
#         except Exception as error:
#             print(error)
#             print(f'the leave is being updated {instance.employee.username} - {instance.leave_date}')


