from django.db import models
from django.utils.text import slugify


class Staff(models.Model):
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=30)
    phone_number = models.IntegerField(max_length=11)
    address = models.CharField()
    iban = models.IntegerField()
    slug = models.SlugField(default="", null=False, db_index=True, blank=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    def save(self, *args, **kwargs):
        self.slug = slugify(self.last_name)
        super().save(*args, **kwargs)