from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import *

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('email', 'username', 'is_staff', 'is_superuser')  # Include 'is_staff' and 'is_superuser'
    search_fields = ('email', 'username')
    readonly_fields = ('last_login',)  

    filter_horizontal = ()
    list_filter = ()
    fieldsets = (
        (None, {'fields': ('email', 'username', 'password')}),
        ('Permissions', {'fields': ('is_staff', 'is_superuser')}),
        ('Important dates', {'fields': ('last_login',)}),
        ('Profile Picture', {'fields': ('profile_picture',)}),  # Add this line for profile picture
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'password1', 'password2', 'is_staff', 'is_superuser', 'profile_picture')}  # Include profile_picture in add fieldsets
        ),
    )

admin.site.register(CustomUser, CustomUserAdmin)




@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'deadline', 'status', 'user')
    list_filter = ('status', 'user')
    search_fields = ('title', 'description', 'user__username')
