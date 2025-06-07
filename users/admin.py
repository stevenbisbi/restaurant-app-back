from django.contrib import admin
from .models import User, Staff, Customer

# Register your models here.
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
  list_display = ('email', 'first_name', 'last_name', 'role', 'is_staff')
  list_filter = ('role', 'is_staff')
  search_fields = ('email', 'fist_name', 'last_name',)
  ordering = ('email',)
  fieldsets = (
    (None, {'fields': ('email', 'password')}),
    ('information personal', {'fields': ('first_name', 'last_name', 'phone_number', 'role')}),
    ('Permisos', {'fields': ('is_active', 'is_staff', 'is_superuser')}),
  )
  add_fieldsets = (
    (None, {
      'classes': ('wide',),
      'fields': ('email', 'first_name', 'last_name', 'phone_number', 'role', 'password1', 'password2'),
    }),
  )

admin.site.register(Staff)
admin.site.register(Customer)