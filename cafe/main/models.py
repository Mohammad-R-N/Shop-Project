from django.db import models


class SiteConfig(models.Model):
    logo = models.ImageField(upload_to="config/logo/")
    background_image = models.ImageField(
        upload_to="config/background/", null=True, blank=True
    )
