from django.contrib import admin

from platforms.models import Platform, OfflineSearchText


class OfflineSearchTextInline(admin.StackedInline):
    """
    Offline Search Text inline.
    """
    model = OfflineSearchText

    fields = [
        "search_text"
    ]
    extra = 1


@admin.register(Platform)
class PlatformAdmin(admin.ModelAdmin):
    """
    Platform model admin.
    """
    inlines = [OfflineSearchTextInline]
    fields = [
        "name",
    ]
    list_display = [
        "name",
    ]
