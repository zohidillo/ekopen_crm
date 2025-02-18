from django.db import models


class CustomManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset()


class BaseModel(models.Model):
    added_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    created_by = models.ForeignKey(
        "core.CustomUser", on_delete=models.SET_NULL, blank=True, null=True,
        related_name='%(app_label)s_%(class)s_created_by', )
    modified_by = models.ForeignKey("core.CustomUser", on_delete=models.SET_NULL,
                                    blank=True, null=True, related_name='%(app_label)s_%(class)s_modified_by')

    objects = CustomManager()

    class Meta:
        abstract = True
