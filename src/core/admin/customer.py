from django.contrib import admin

import src.core.models as models


@admin.register(models.Customer)
class CustomerAdmin(admin.ModelAdmin):
    search_fields = ("first_name", "last_name", "phone_number")
    list_display = ("id", "first_name", "phone_number")
    list_display_links = ("id", "first_name")
