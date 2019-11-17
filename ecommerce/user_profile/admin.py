from django.contrib import admin
from .models import Address, UserProfile

class UserProfileInline(admin.TabularInline):
    model = Address
    max_num = 1

class UserProfileAdmin(admin.ModelAdmin):
    inlines = [
        UserProfileInline
    ]

admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(Address)
