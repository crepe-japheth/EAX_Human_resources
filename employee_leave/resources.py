from import_export import resources

from .models import Leave

class LeaveResource(resources.ModelResource):
    class Meta:
        model = Leave
        fields = ['employee', 'leave_type','leave_date', 'return_date', 'status']

    def dehydrate_employee(self, obj):
        # print(obj.employee.username)
        return str(obj.employee.username)