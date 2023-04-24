from django.contrib import admin
from .models import *


class CustomerAdminModel(admin.ModelAdmin):
    list_display = ['id', 'user', 'name', 'email']
    list_filter = list_display
    list_select_related = ['user']
    list_per_page = 10
    search_fields = ['name', 'email']
    search_help_text = ['Poojan']


class ProductAdminModel(admin.ModelAdmin):
    list_display = ['id', 'name', 'product_category', 'avg_rating']
    list_select_related = ['product_category']
    list_filter = ['id', 'name', 'avg_rating']
    list_per_page = 10
    search_fields = ['name']


class OrderDetailModel(admin.ModelAdmin):
    list_display = ['id', 'product', 'order', 'quantity', 'date_added']
    list_filter = list_display
    list_select_related = ['product', 'order']
    list_per_page = 10


class OrderDetailInlines(admin.StackedInline):
    model = OrderItem


class OrderAdminModel(admin.ModelAdmin):
    inlines = [OrderDetailInlines]
    list_display = ['id', 'customer', 'complete', 'transaction_id']
    list_select_related = ['customer']
    list_filter = list_display
    list_per_page = 10


class ShippingAddressAdminModel(admin.ModelAdmin):
    list_display = ['id', 'customer', 'order', 'address', 'country', 'date_added']
    list_filter = list_display
    list_per_page = 10
    search_fields = ['address']


class ImageAdminModel(admin.ModelAdmin):
    list_display = ['id', 'product', 'image']
    list_filter = list_display
    list_per_page = 10


class RatingAdminModel(admin.ModelAdmin):
    list_display = ['id', 'product', 'user', 'stars']
    list_filter = list_display
    list_per_page = 10


class CategoriesAdminModel(admin.ModelAdmin):
    list_display = ['id', 'product_category']
    list_filter = list_display
    list_per_page = 10


admin.site.register(Customer, CustomerAdminModel)
admin.site.register(Product, ProductAdminModel)
admin.site.register(Order, OrderAdminModel)
admin.site.register(OrderItem, OrderDetailModel)
admin.site.register(ShippingAddress, ShippingAddressAdminModel)
admin.site.register(Image, ImageAdminModel)
admin.site.register(Rating, RatingAdminModel)
admin.site.register(Categories, CategoriesAdminModel)
