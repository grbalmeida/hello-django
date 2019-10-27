from django.contrib import admin
from .models import Category, Contact

class ContactAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'last_name',
        'phone',
        'email',
        'creation_date',
        'category',
        'show'
    )

    list_display_links = (
        'id',
        'name',
        'last_name'
    )

    list_filter = (
        'name',
        'last_name'
    )

    search_fields = (
        'name',
        'last_name',
        'phone'
    )

    list_editable = (
        'phone',
        'show'
    )

    list_per_page = 10

class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name'
    )

    list_display_links = (
        'id',
        'name'
    )

    search_fields = (
        'name',
    )

    list_per_page = 10

admin.site.register(Category, CategoryAdmin)
admin.site.register(Contact, ContactAdmin)
