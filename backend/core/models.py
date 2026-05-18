from django.db import models


class BaseModel(models.Model):
    class Meta:
        abstract = True

    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

