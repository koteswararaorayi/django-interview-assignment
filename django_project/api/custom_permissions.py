from rest_framework.permissions import BasePermission

class IsLibrarian(BasePermission):
   def has_permission(self, request, view):
      return request.user.role=="LIBRARIAN" 