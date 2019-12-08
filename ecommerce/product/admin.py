from django.contrib import admin
from .models import Product, Variation

class VariationInline(admin.TabularInline):
    model = Variation
    extra = 1

class ProductAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'short_description',
        'get_formatted_price_marketing',
        'get_formatted_promotional_price_marketing'
    )

    inlines = [
        VariationInline
    ]

admin.site.register(Product, ProductAdmin)
admin.site.register(Variation)
