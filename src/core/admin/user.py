from django.contrib import admin

import src.core.models as models


@admin.register(models.CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ("id", "username", "role")
    list_display_links = ("id", "username",)
    filter_horizontal = ("user_permissions", "groups")
    readonly_fields = ("password", "last_login", "date_joined")
