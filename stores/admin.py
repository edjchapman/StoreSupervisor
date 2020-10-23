from django.contrib import admin

from stores.models import Store, StoreFront, StoreAudit, DayOpeningOverride


class StoreFrontInline(admin.TabularInline):
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
    extra = 0


class DayOpeningOverrideInline(admin.TabularInline):
    """
    Day Opening Inline.
    """
    model = DayOpeningOverride
    fields = [
        "day",
        "open_time",
        "close_time",
        "closed"
    ]
    extra = 0


@admin.register(Store)
class StoreAdmin(admin.ModelAdmin):
    """
    Store model admin.
    """
    fields = [
        "name",
        "address",
        "phone",
        "open_time",
        "close_time",
    ]
    list_display = [
        "name",
        "open_time",
        "close_time"
    ]
    inlines = [
        DayOpeningOverrideInline,
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
