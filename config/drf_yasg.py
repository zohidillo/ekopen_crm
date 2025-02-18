from drf_yasg import openapi
from django.contrib import admin
from rest_framework import permissions
from drf_yasg.views import get_schema_view

API_TITLE = 'Ekopen Chinobod'
API_DESCRIPTION = 'Ekopen Chinobod documents'

yasg_schema_view = get_schema_view(
    openapi.Info(
        title=API_TITLE,
        default_version='v1',
        description=API_DESCRIPTION,
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="turgunovzohidillo77@gmail.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

admin.site.site_header = "Ekopen Chinobod"
admin.site.site_title = "Ekopen Chinobod"
admin.site.index_title = "Ekopen Chinobod"
