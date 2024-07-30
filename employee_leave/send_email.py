from django.core.mail import send_mail

def leave_message(employee_name, leave_date, return_date, status, leave_reason):
    msg = ''
    if status == "cancelled":
        msg = f'''
        Dear {employee_name},

        I hope this mail finds you well, we regret to inform you that your recent leave request for {leave_date} cannot be approved at this time. 

        We understand the importance of taking time off and assure you that we aim to accommodate your requests whenever possible. Please feel free to reach out if you have any further questions.

        Thank you for your understanding.

        Best regards,
        EAX Leave Management APP
        EAX / HR Management'''
    elif status == 'approved':

        msg = f'''Dear {employee_name},

        We are writing to confirm that your leave request for {leave_date} has been approved. Your time off has been scheduled accordingly in our system.

        We hope you have a restful and rejuvenating time during your leave. If there are any changes or if you have any questions, feel free to reach out to [HR/Management contact] for assistance.

        Please log in to the [App/Platform] to see your approval.

        Thank you.

        Best regards,

        EAX Leave Management APP'''
    else:

        msg = f'''Dear HR Manager(s),

        {employee_name} has submitted a leave request through the [App/Platform]. Please review the details below:

        - Requested Dates: {leave_date} to {return_date}
        - Reason for Leave: {leave_reason}

        Please log in to the [App/Platform] to approve or manage this request at your earliest convenience.

        Thank you.

        Best regards,

        EAX Leave Management APP
        '''
    return msg

def send_mail_to_employee(employee_email, leave_date, return_date, status, employee_name, leave_reason):
    subject = f'leave request {status}'
    message = leave_message(employee_name, leave_date, return_date, status, leave_reason)

    send_mail(
        subject=subject, 
        message=message, 
        recipient_list=[employee_email], 
        from_email=None, 
        fail_silently=False
        )


# EMAIL PASSWORD = zdia cpwp dvlz esvv