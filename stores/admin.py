from django.contrib import admin

from stores.models import Store, StoreFront, StoreAudit


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
        "close_time",
        "monday",
        "tuesday",
        "wednesday",
        "thursday",
        "friday",
        "saturday",
        "sunday"
    ]
    list_display = [
        "name",
        "open_time",
        "close_time"
    ]
    inlines = [
        StoreFrontInline
    ]


@admin.register(StoreAudit)
class StoreAuditAdmin(admin.ModelAdmin):
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
