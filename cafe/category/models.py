from django.db import models



class Category(models.Model):
    name = models.TextField(max_length=60)
    photo = models.ImageField(upload_to='media/img')
    slug = models.SlugField(default="", null=False, db_index=True, blank=True)

    def __str__(self):
        return f"{self.name}"


