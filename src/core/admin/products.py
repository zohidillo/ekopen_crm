from django.contrib import admin

import src.core.models as models


@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    search_fields = ("name",)
    list_per_page = 20
    list_display_links = ("id", "name")
    list_display = ("id", "name", "category", "measurement")


@admin.register(models.ProductCategory)
class ProductCategoryAdmin(admin.ModelAdmin):
    list_per_page = 20
    search_fields = ("name",)
    list_display = ("id", "name")
    list_display_links = ("id", "name")


@admin.register(models.ProductMeasurement)
class ProductMeasurementAdmin(admin.ModelAdmin):
    list_per_page = 20
    search_fields = ("name",)
    list_display = ("id", "name")
    list_display_links = ("id", "name")
