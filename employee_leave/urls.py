from django.urls import path
from .views import homepage, leave, employee, ProfileView, CustomPasswordChangeView

urlpatterns = [
    path('', homepage, name='home'),
    path('leave/', leave, name='leave'),
    path('employee/', employee, name='employee'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path("change_password/", CustomPasswordChangeView.as_view(), name="change_password"),
]