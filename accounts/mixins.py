from django.contrib.auth.mixins import UserPassesTestMixin
from django.core.exceptions import PermissionDenied

class RoleRequiredMixin(UserPassesTestMixin):
    allowed_roles = []

    def test_func(self):
        if not self.request.user.is_authenticated:
            return False
        return self.request.user.role in self.allowed_roles or self.request.user.is_superuser

    def handle_no_permission(self):
        if self.request.user.is_authenticated:
            raise PermissionDenied("You do not have permission to access this page.")
        return super().handle_no_permission()

class AdminRequiredMixin(RoleRequiredMixin):
    allowed_roles = ['Admin']

class ReceptionistOrAdminRequiredMixin(RoleRequiredMixin):
    allowed_roles = ['Admin', 'Receptionist']

class DoctorRequiredMixin(RoleRequiredMixin):
    allowed_roles = ['Doctor']

class DoctorOrAdminRequiredMixin(RoleRequiredMixin):
    allowed_roles = ['Admin', 'Doctor']
