from django.urls import path
from .views import homepage, leave, employee, ProfileView, CustomPasswordChangeView, supervisor_change_status, supervisor_approve, supervisor_cancel

urlpatterns = [
    path('', homepage, name='home'),
    path('leave/', leave, name='leave'),
    path('employee/', employee, name='employee'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('supervisor_leaves/', supervisor_change_status, name='supervisor_leaves'),
    path('supervisor_approve/<int:pk>/', supervisor_approve, name='supervisor_approve'),
    path('supervisor_cancel/<int:pk>/', supervisor_cancel, name='supervisor_cancel'),
    path("change_password/", CustomPasswordChangeView.as_view(), name="change_password"),
]