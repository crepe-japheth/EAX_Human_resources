from django.contrib import admin
from .models import Employee, Leave
from django.contrib.auth.models import Group
from .resources import LeaveResource
from import_export.admin import ExportMixin

class LeaveAdmin(ExportMixin, admin.ModelAdmin):
    readonly_fields = ('employee','leave_type','leave_date','return_date','comment')
    list_display = ['employee', 'leave_type','leave_date', 'return_date', 'status']
    resource_class = LeaveResource
    list_export = ('xlsx', 'pdf', 'csv',)


    def has_add_permission(self, request, obj=None):
        return False
    
    def has_delete_permssion(self, request, obj=None):
        return False
    


class EmployeeAdmin(admin.ModelAdmin):
    list_display = ['user', 'sex', 'position', 'hire_date']


admin.site.register(Employee, EmployeeAdmin)
admin.site.register(Leave, LeaveAdmin)
admin.site.unregister(Group)


admin.site.site_header = 'EAX'                    
admin.site.index_title = 'EAX '                
admin.site.site_title = 'EAX'
