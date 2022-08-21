from django.contrib import admin
from .models import Profile


class ProfileAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'newsletter_subscription']
    search_fields = ('user__username', 'user__email' )


admin.site.register(Profile, ProfileAdmin)
