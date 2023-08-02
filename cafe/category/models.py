from django.db import models
from django.utils.text import slugify


class Category(models.Model):
    name = models.TextField(max_length=60)
    photo = models.ImageField(upload_to='media/img')
    slug = models.SlugField(default="", null=False, db_index=True, blank=True)

    def __str__(self):
        return f"{self.name}"

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)
