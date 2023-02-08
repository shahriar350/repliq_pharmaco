from rest_framework.permissions import BasePermission


class IsMerchant(BasePermission):
    """
    The request is authenticated as a user, or is a read-only request.
    """

    def has_permission(self, request, view):
        return bool(
            request.user and
            request.user.is_authenticated and (
                    request.user.groups.filter(name="merchant_owner").exists() or
                    request.user.groups.filter(name="merchant_admin").exists() or
                    request.user.groups.filter(name="merchant_staff").exists()
            )
        )


class IsMerchantOwner(BasePermission):
    """
    The request is authenticated as a user, or is a read-only request.
    """

    def has_permission(self, request, view):
        return bool(
            request.user and
            request.user.is_authenticated and
            request.user.groups.filter(name="merchant_owner").exists()

        )


class IsMerchantOwnerOrAdmin(BasePermission):
    """
    The request is authenticated as a user, or is a read-only request.
    """

    def has_permission(self, request, view):
        return bool(
            request.user and
            request.user.is_authenticated and (
                    request.user.groups.filter(name="merchant_owner").exists() or
                    request.user.groups.filter(name="merchant_admin").exists()
            )
        )


class IsMerchantAdmin(BasePermission):
    """
    The request is authenticated as a user, or is a read-only request.
    """

    def has_permission(self, request, view):
        return bool(
            request.user and
            request.user.is_authenticated and
            request.user.groups.filter(name="merchant_owner").exists()

        )


class IsMerchantStaff(BasePermission):
    """
    The request is authenticated as a user, or is a read-only request.
    """

    def has_permission(self, request, view):
        return bool(
            request.user and
            request.user.is_authenticated and
            request.user.groups.filter(name="merchant_staff").exists()

        )


class IsSuperAdminOrAdmin(BasePermission):
    """
    The request is authenticated as a user, or is a read-only request.
    """

    def has_permission(self, request, view):
        return bool(
            request.user and
            (
                    request.user.is_superuser and
                    request.user.admin
            )
        )
