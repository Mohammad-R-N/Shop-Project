from django.contrib import admin
from .models import Category
from .models import Product
# Register your models here.




class ProductAdmin(admin.ModelAdmin):

    actions = ['make_inactive']

    @admin.action(description='Mark selected product as inactive')
    def make_inactive(self, request, queryset):
        queryset.update(status='not_active')

    search_fields = ['name', 'description']
    list_display = ['name', 'price', 'category_menu', 'status']
    list_filter = ['status']
    readonly_fields = ['img_preview']
    list_per_page = 2


class CategoryAdmin(admin.ModelAdmin):
    search_fields = ['name']
    list_display = ['name']
    list_per_page = 2


admin.site.register(Product, ProductAdmin)
admin.site.register(Category, CategoryAdmin)
