from django.contrib import admin

from .models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    """User admin class."""
    list_display = ('pk', 'username', 'first_name', 'last_name', 'email',
                    'is_superuser', 'is_staff',)
    search_fields = ('username',)
    list_filter = ('first_name', 'email',)
    list_editable = ('is_superuser', 'is_staff')
    empty_value_display = '-пусто-'
