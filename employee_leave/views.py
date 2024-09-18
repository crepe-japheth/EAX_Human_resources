from django.shortcuts import render, redirect
from .models import Employee, Leave
from django.contrib.auth.decorators import login_required
import datetime
from django.db.models import Count
from .annual_leave_calc import calc_annual, calc_marternity_leave, calc_parternity_leave, calc_sabbatical_leave, calc_sick_leave
from django.contrib import messages
from django.views.generic.base import TemplateView
from django.contrib.auth.views import PasswordChangeView
from django.contrib.auth.forms import PasswordChangeForm
from django.urls import reverse_lazy
from django.contrib.auth import update_session_auth_hash

@login_required(login_url="/login")
def homepage(request):
    if request.user.first_login:
        return redirect('change_password')
    if request.user.is_superuser:
        employees = Employee.objects.all()
        all_leaves = Leave.objects.all()

        number = employees.count()
        leaves = all_leaves.filter(leave_date=datetime.date.today())
        total_leaves = all_leaves.filter(leave_date__month=datetime.datetime.now().month)
        leaves_pending = all_leaves.filter(leave_date=datetime.date.today(), status='pending').count()

        today_leaves = leaves.count()
        total_month_leave = total_leaves.values('leave_date').annotate(Count('leave_date'))
        total_leave_type_count = total_leaves.values('leave_type').annotate(Count('leave_type'))
        context = {
            'card1_value':number, 
            'card2_value':today_leaves, 
            'card3_value':leaves_pending, 
            'card1_text':'Total Employees', 
            'card2_text':'Today Total leaves', 
            'card3_text':'Today pending leaves', 
            'employees':employees, 
            'total_leave_type':total_leave_type_count, 
            'total_month_leave':total_month_leave
            }
        return render(request, 'index.html', context )
    else:
        if hasattr(request.user, 'employee'):
            employees = Employee.objects.filter(user=request.user)[0]
            all_leaves = Leave.objects.filter(employee=request.user, leave_date__month=datetime.datetime.now().month)
            total_allowed_leaves = employees.initial_leave
            taken_leave = int(employees.taken_leave)
            remaining_leave = int(employees.allowed_leave)

            total_leave = all_leaves.values('leave_date').annotate(Count('leave_date'))
            total_leave_type = all_leaves.values('leave_type').annotate(Count('leave_type'))

            context = {
                'card1_value':total_allowed_leaves,
                'card2_value':taken_leave,
                'card3_value':remaining_leave,
                'card1_text':'Total Leaves', 
                'card2_text':'Taken leaves', 
                'card3_text':'Remaining leaves',
                'total_leave_type':total_leave_type,
                'total_month_leave':total_leave
            }
        else:
            context = {
                'card1_value':"No employee assigned",
                'card2_value':"No employee assigned",
                'card3_value':"No employee assigned",
                'card1_text':'Total Leaves', 
                'card2_text':'Taken leaves', 
                'card3_text':'Remaining leaves',
                'total_leave_type':"none",
                'total_month_leave':"none"
            }

        return render(request, 'index.html', context)


@login_required(login_url="/login")
def employee(request):
    if request.user.first_login:
        return redirect('change_password')
    employees = Employee.objects.all()
    context = {
        'employees':employees
    }
    return render(request, 'employee.html', context)

@login_required(login_url="/login")
def leave(request):
    if request.user.first_login:
        return redirect('change_password')
    if request.method == 'POST':
        leave_type = request.POST.get('leave_type')
        leave_date = request.POST.get('leaving_date')
        returning_date = request.POST.get('returning_date')
        comment = request.POST.get('comment')
        # checking the leave past date and overlapping leave request
        # 
        # 
        #  # Convert string dates to datetime objects for comparison
        leave_date_obj = datetime.datetime.strptime(leave_date, '%Y-%m-%d')
        returning_date_obj = datetime.datetime.strptime(returning_date, '%Y-%m-%d')

        # Check if the leave dates are in the past
        if leave_date_obj.date() < datetime.datetime.today().date():
            messages.error(request, 'Sorry!!, you cannot request leave for past dates.')
            return redirect('home')

        # Check if the requested leave dates overlap with any previous leaves
        overlapping_leaves = Leave.objects.filter(
            employee=request.user,
            leave_date__lte=returning_date_obj,
            return_date__gte=leave_date_obj
        )

        if overlapping_leaves.exists():
            messages.error(request, 'Sorry!!, you have already requested leave during this period.')
            return redirect('home') 


        if leave_type == 'paid_leave':
            if calc_annual(leave_date, returning_date)[0] == False:
                messages.error(request, 'Sorry!!, you cannot take more than 18 days for annual paid leave')
                return redirect('home')
            elif calc_annual(leave_date, returning_date)[1] > request.user.employee.allowed_leave:
                messages.error(request, 'Sorry!!, you cannot take more than remaining days for annual paid leave')
                return redirect('home')

            else:
                leave_obj = Leave(employee=request.user, leave_type=leave_type, leave_date=leave_date, return_date=returning_date, comment=comment)
                leave_obj.save()
                # employee_obj = request.user.employee
                # employee_obj.allowed_leave = employee_obj.allowed_leave - calc_annual(leave_date, returning_date)[1]
                # employee_obj.taken_leave = employee_obj.taken_leave + calc_annual(leave_date, returning_date)[1]
                # employee_obj.save()
                messages.success(request, 'Your leave request have been sent')
                return redirect('home')
        elif leave_type == 'sick_leave':
            if calc_sick_leave(leave_date, returning_date) == False:
                messages.error(request, 'Sorry!!, you cannot take more than 90 days for Sick leave')
                return redirect('home')
            else:
                leave_obj = Leave(employee=request.user, leave_type=leave_type, leave_date=leave_date, return_date=returning_date, comment=comment)
                leave_obj.save()
                messages.success(request, 'Your leave request have been sent')
                return redirect('home')
        elif leave_type == 'marternity_leave':
            if calc_marternity_leave(leave_date, returning_date) == False:
                messages.error(request, 'Sorry!!, you cannot take more than 90 days for Marternity leave')
                return redirect('home')
            else:
                leave_obj = Leave(employee=request.user, leave_type=leave_type, leave_date=leave_date, return_date=returning_date, comment=comment)
                leave_obj.save()
                messages.success(request, 'Your leave request have been sent')
                return redirect('home')
    
        elif leave_type == 'parternity_leave':
            if calc_parternity_leave(leave_date, returning_date) == False:
                messages.error(request, 'Sorry!!, you cannot take more than 4 days for Parternity leave')
                return redirect('home')
            else:
                leave_obj = Leave(employee=request.user, leave_type=leave_type, leave_date=leave_date, return_date=returning_date, comment=comment)
                leave_obj.save()
                messages.success(request, 'Your leave request have been sent')
                return redirect('home')
        elif leave_type == 'sabbatical_leave':
            if calc_sabbatical_leave(leave_date, returning_date) == False:
                messages.error(request, 'Sorry!!, you cannot take more than 90 days for Sabbatical leave')
                return redirect('home')
            else:
                leave_obj = Leave(employee=request.user, leave_type=leave_type, leave_date=leave_date, return_date=returning_date, comment=comment)
                leave_obj.save()
                messages.success(request, 'Your leave request have been sent')
                return redirect('home')
    
    else:
        applied_leave = Leave.objects.filter(employee=request.user)
        return render(request, 'leave.html', {'leaves':applied_leave})



class ProfileView(TemplateView):
    template_name = 'profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if hasattr(self.request.user, 'employee'):
            employee = Employee.objects.get(user=self.request.user)
            context['employee'] = employee
        return context
    


class CustomPasswordChangeView(PasswordChangeView):
    form_class = PasswordChangeForm
    template_name = 'registration/change_password.html'
    success_message = 'Password changed successfully!'
    success_url = reverse_lazy('home') 

    def form_valid(self, form):
        self.request.user.first_login = False
        self.request.user.save()
        return super().form_valid(form)

