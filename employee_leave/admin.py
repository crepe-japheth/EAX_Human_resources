from django.contrib import admin
from .models import Employee, Leave, NextOfKeen, EmployeeAttachment , Department
from django.contrib.auth.models import Group
from .resources import LeaveResource
from import_export.admin import ExportMixin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import CustomUser

class CustomUserAdmin(BaseUserAdmin):
    model = CustomUser
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        # ('Personal info', {'fields': ('first_name', 'last_name', 'email')}),
        ('Permissions', {
            'fields': ('is_active', 'is_staff', 'is_superuser'),
        }),
    )
    filter_horizontal = ()

    def save_model(self, request, obj, form, change):
        if 'password' in form.changed_data:
            obj.first_login = True
        super().save_model(request, obj, form, change)




class LeaveAdmin(ExportMixin, admin.ModelAdmin):
    readonly_fields = ('employee', 'supervisor_status','leave_type','leave_date','return_date','comment')
    list_display = ['employee', 'leave_type','leave_date', 'return_date', 'status']
    resource_class = LeaveResource
    list_export = ('xlsx', 'pdf', 'csv',)


    def has_add_permission(self, request, obj=None):
        return False
    
    def has_delete_permssion(self, request, obj=None):
        return False
    



class EmployeeAttachmentInline(admin.TabularInline):
    model = EmployeeAttachment
    extra = 1  

class NextOfKeenInline(admin.TabularInline):
    model = NextOfKeen
    extra = 1  

class EmployeeAdmin(admin.ModelAdmin):
    inlines = [EmployeeAttachmentInline, NextOfKeenInline]
    list_display = ['first_name', 'last_name', 'sex', 'position', 'hire_date']
    # readonly_fields = ('taken_leave', allowed_leave, initial_leave)
    # exclude = ['initial_leave',]

class DepartmentAdmin(admin.ModelAdmin):
    list_display = ['department_name', 'department_head']


    
# Unregister the default User admin
# admin.site.unregister(User)
try:
    admin.site.unregister(CustomUser)
except admin.sites.NotRegistered:
    pass

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Employee, EmployeeAdmin)
admin.site.register(Department, DepartmentAdmin)
admin.site.register(Leave, LeaveAdmin)
admin.site.unregister(Group)


admin.site.site_header = 'EAX'                    
admin.site.index_title = 'EAX '                
admin.site.site_title = 'EAX'
