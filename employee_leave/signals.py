from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from .send_email import send_mail_to_employee
from .models import Employee, CustomUser, Leave


@receiver(post_save, sender=Leave)
def leave_created_signal(sender, instance, created, **kwargs):
    if created:
        try:
            send_mail_to_employee("nshimiyaaron87@gmail.com", instance.leave_date, instance.return_date,instance.status, instance.employee.username, instance.leave_type)
        except:
            print(f'the leave is being applied {instance.employee.username} - {instance.leave_date}')
    else:
        if instance.status == 'approved':
            employee = Employee.objects.filter(user=instance.employee)[0]
            employee.taken_leave +=1
            employee.save()
        try:
            send_mail_to_employee(instance.employee.email, instance.leave_date, instance.return_date,instance.status, instance.employee.username, instance.leave_type)
        except:
            print(f'the leave is being updated {instance.employee.username} - {instance.leave_date}')



