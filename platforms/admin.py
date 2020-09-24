from django.contrib import admin

from platforms.models import Platform


@admin.register(Platform)
class PlatformAdmin(admin.ModelAdmin):
    """
    Platform model admin.
    """
    fields = [
        "name",
        "offline_search_text",
    ]
    list_display = [
        "name",
        "offline_search_text",
    ]
