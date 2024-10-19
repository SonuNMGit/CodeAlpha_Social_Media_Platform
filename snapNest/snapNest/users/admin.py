from django.contrib import admin
from django.contrib.auth.models import User
from .models import UserProfile
from django.utils.html import mark_safe

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'profile_photo_display', 'bio', 'privacy')
    search_fields = ['user__username', 'user__email']
    list_filter = ['privacy']
    
    def profile_photo_display(self, obj):
        if obj.profile_photo:
            return mark_safe(f'<img src="{obj.profile_photo.url}" width="50" height="50" />')
        return "-"
    profile_photo_display.short_description = 'Profile Photo'

admin.site.register(UserProfile, UserProfileAdmin)

class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_active', 'is_staff')
    search_fields = ['username', 'email']
    list_filter = ['is_active', 'is_staff']

admin.site.unregister(User)
admin.site.register(User, UserAdmin)

