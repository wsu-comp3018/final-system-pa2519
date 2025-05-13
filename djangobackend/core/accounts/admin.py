from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from accounts.models import User

class UserModelAdmin(BaseUserAdmin):
    list_display = ('id', 'email', 'first_name', 'last_name', 'is_admin')
    list_filter = ('is_admin')
    fieldsets = (
        ('User Credentials', {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name')}),
        ('Permissions', {'fields': ('is_admin')}),
    )

    add_fieldsets = (
        (None,
            {
                'classes': ['wide'],
                'fields': ['email','first_name','last_name','password1','password2']
            }
        ),
    )

    search_fields = ('email')
    ordering = ('email','id')
    filter_horizontal=()

#now register the new UserModelAdmin
admin.site.register(User, UserModelAdmin)