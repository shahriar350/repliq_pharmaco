from rest_framework.permissions import BasePermission


class IsOrganization(BasePermission):
	"""
	Anyone who works in an organization, whatever his role, can access this normal organization permission.
	Only need to a authorize role of this organization.
	"""

	def has_permission(self, request, view):
		if request.user.is_authenticated and (request.user.get_organization() is not None):
			return True
		return False


class IsOrganizationOwner(BasePermission):
	"""
	Only Owner can access this owner permission
	"""

	def has_permission(self, request, view):
		if request.user.is_authenticated and request.user.get_my_organization_role() == 'owner':
			return True
		return False


class IsOrganizationAdmin(BasePermission):
	"""
	Only Owner or Admin can access this admin permission
	"""

	def has_permission(self, request, view):
		if request.user.is_authenticated and (
				request.user.get_my_organization_role() == 'admin' or
				request.user.get_my_organization_role() == 'owner'):
			return True
		return False


class IsOrganizationStaff(BasePermission):
	"""
	Owner, Admin or Staff anyone can access this staff permission
	"""

	def has_permission(self, request, view):
		if request.user.is_authenticated and (
				request.user.get_my_organization_role() == 'owner' or
				request.user.get_my_organization_role() == 'admin' or
				request.user.get_my_organization_role() == 'staff'
		):
			return True
		return False
