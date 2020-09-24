from django.contrib import admin

from stores.models import Store, StoreFront, StoreFrontStatusLog


class StoreFrontInline(admin.StackedInline):
    """
    Store Front inline.
    """
    model = StoreFront
    fields = [
        "platform",
        "url",
        "store",
        "status",
        "online"
    ]
    readonly_fields = [
        "online"
    ]
    extra = 1


@admin.register(Store)
class StoreAdmin(admin.ModelAdmin):
    """
    Store model admin.
    """
    fields = [
        "name",
        "open_time",
        "close_time"
    ]
    list_display = [
        "name",
        "open_time",
        "close_time"
    ]
    inlines = [
        StoreFrontInline
    ]


@admin.register(StoreFrontStatusLog)
class StoreFrontStatusLogAdmin(admin.ModelAdmin):
    """
    Store Front Status Log admin.
    """
    fields = [
        "store_front",
        "online",
        "log_time",
    ]
    list_display = [
        "store_front",
        "online",
        "log_time"
    ]
    list_filter = [
        "store_front",
        "online",
        "log_time"
    ]
