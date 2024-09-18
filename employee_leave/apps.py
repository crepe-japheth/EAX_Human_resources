# from django.apps import AppConfig
# from .scheduler import start_scheduler


# class EmployeeLeaveConfig(AppConfig):
#     default_auto_field = 'django.db.models.BigAutoField'
#     name = 'employee_leave'

#     def ready(self):
#         import employee_leave.signals
#         start_scheduler()

from django.apps import AppConfig
import threading

class EmployeeLeaveConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'employee_leave'

    def ready(self):
        import employee_leave.signals

        # Start the scheduler in a separate thread to avoid blocking the main thread
        # def start_scheduler():
        #     from .scheduler import start_scheduler
        #     start_scheduler()
        #     print("started Job scheduler ...")

        # threading.Thread(target=start_scheduler).start()
