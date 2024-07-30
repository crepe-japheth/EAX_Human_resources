from django.shortcuts import render, redirect
from .models import Employee, Leave
from django.contrib.auth.decorators import login_required
import datetime
from django.db.models import Count
from .annual_leave_calc import calc_annual
from django.contrib import messages

@login_required(login_url="/login")
def homepage(request):
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
        employees = Employee.objects.filter(user=request.user)[0]
        all_leaves = Leave.objects.filter(employee=request.user, leave_date__month=datetime.datetime.now().month)
        total_allowed_leaves = employees.allowed_leave
        taken_leave = employees.taken_leave
        remaining_leave = total_allowed_leaves - taken_leave 

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

        return render(request, 'index.html', context)

def employee(request):
    employees = Employee.objects.all()
    context = {
        'employees':employees
    }
    return render(request, 'employee.html', context)

@login_required(login_url="/login")
def leave(request):
    if request.method == 'POST':
        leave_type = request.POST.get('leave_type')
        leave_date = request.POST.get('leaving_date')
        returning_date = request.POST.get('returning_date')
        comment = request.POST.get('comment')
        if leave_type == 'paid_annual':
            if calc_annual(leave_date, returning_date) == False:
                messages.error(request, 'Sorry!!, you cannot take more than 18 days for annual paid leave')
                return redirect('home')
            else:
                leave_obj = Leave(employee=request.user, leave_type=leave_type, leave_date=leave_date, return_date=returning_date, comment=comment)
                leave_obj.save()
                messages.success(request, 'Your leave request have been sent')
                return redirect('home')
        else:
            leave_obj = Leave(employee=request.user, leave_type=leave_type, leave_date=leave_date, return_date=returning_date, comment=comment)
            leave_obj.save()
            messages.success(request, 'Your leave request have been sent')
            return redirect('home')
    else:
        applied_leave = Leave.objects.filter(employee=request.user)
        return render(request, 'leave.html', {'leaves':applied_leave})

