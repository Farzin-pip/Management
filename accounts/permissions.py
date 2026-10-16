# from rest_framework.permissions import BasePermission
#
#
# class IsAuthenticatedUser(BasePermission):
#
#     def has_permission(self, request, view):
#         return request.user.is_authenticated
#
#
# class IsAdmin(BasePermission):
#
#     def has_permission(self, request, view):
#         return (
#             request.user.is_authenticated
#             and request.user.role == 'admin'
#         )
#
#
# class IsAdminOrManager(BasePermission):
#
#     def has_permission(self, request, view):
#         return (
#             request.user.is_authenticated
#             and request.user.role in [
#                 'admin',
#                 'manager'
#             ]
#         )
#
#
# class IsAdminOrAccountant(BasePermission):
#
#     def has_permission(self, request, view):
#         return (
#             request.user.is_authenticated
#             and request.user.role in [
#                 'admin',
#                 'accountant'
#             ]
#         )
#
#
# class IsAdminManagerOrAccountant(BasePermission):
#
#     def has_permission(self, request, view):
#         return (
#             request.user.is_authenticated
#             and request.user.role in [
#                 'admin',
#                 'manager',
#                 'accountant'
#             ]
#         )
#
#
# class FacilityBookingPermission(BasePermission):
#
#     def has_permission(self, request, view):
#
#         if not request.user.is_authenticated:
#             return False
#
#         if request.method == 'GET':
#             return True
#
#         return request.user.role in [
#             'admin',
#             'manager',
#             'resident'
#         ]
#
#
# class FacilityBookingObjectPermission(BasePermission):
#
#     def has_object_permission(self, request, view, obj):
#
#         if request.user.role in [
#             'admin',
#             'manager'
#         ]:
#             return True
#
#         return obj.user_id == request.user
#
#
# class ResidentUnitPermission(BasePermission):
#
#     def has_permission(self, request, view):
#
#         if not request.user.is_authenticated:
#             return False
#
#         return request.user.role in [
#             'admin',
#             'manager',
#             'resident'
#         ]
#
#     def has_object_permission(self, request, view, obj):
#
#         if request.user.role in [
#             'admin',
#             'manager'
#         ]:
#             return True
#
#         return obj.tenancies.filter(
#             user=request.user,
#             end_date__isnull=True
#         ).exists()