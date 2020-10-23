from django.db import models
from django.utils import timezone as tz


class Store(models.Model):
    """
    Store model
    """
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=255)
    phone = models.CharField(max_length=50)
    open_time = models.TimeField()
    close_time = models.TimeField()

    def __str__(self):
        return self.name

    def should_be_open(self, now=None):
        do = self.dayopeningoverride_set.filter(day=now.weekday()).first()
        if do:
            if do.closed:
                return False
            return self.open_now(do.open_time, do.close_time)
        return self.open_now(self.open_time, self.close_time)

    @staticmethod
    def open_now(open_time, close_time, now=None):
        now = now or tz.localtime()
        if open_time > close_time:  # e.g. 12:00 - 06:00
            if now > open_time or now < close_time:
                return True
        elif open_time < close_time:  # e.g. 06:00 - 24:00
            if open_time < now < close_time:
                return True
        elif open_time == close_time:  # 24 Hours
            return True


class DayOpeningOverride(models.Model):
    """
    Day Opening Time, overrides the standard opening time.
    """
    DAYS_OF_WEEK = (
        (0, 'Monday'),
        (1, 'Tuesday'),
        (2, 'Wednesday'),
        (3, 'Thursday'),
        (4, 'Friday'),
        (5, 'Saturday'),
        (6, 'Sunday'),
    )
    store = models.ForeignKey('stores.Store', on_delete=models.CASCADE)
    day = models.IntegerField(choices=DAYS_OF_WEEK)
    open_time = models.TimeField(null=True, blank=True)
    close_time = models.TimeField(null=True, blank=True)
    closed = models.BooleanField(default=False)

    class Meta:
        unique_together = ("store", "day")

    def __str__(self):
        return "Opening Time Override: {} {}".format(
            self.store.name,
            self.get_day_display()
        )


class StoreFront(models.Model):
    """
    Store Front model.
    """
    ACTIVE = "ACTIVE"
    DISABLED = "DISABLED"
    STATUS_CHOICES = [
        (ACTIVE, "Active"),
        (DISABLED, "Disabled"),
    ]
    platform = models.ForeignKey("platforms.Platform", on_delete=models.CASCADE)
    url = models.URLField()
    store = models.ForeignKey("stores.Store", on_delete=models.CASCADE)
    status = models.CharField(max_length=100, default=ACTIVE, choices=STATUS_CHOICES)
    online = models.BooleanField(default=False, editable=False)

    class Meta:
        unique_together = ["store", "platform"]

    def __str__(self):
        return "{} - {}".format(
            self.store.name,
            self.platform.name
        )


class StoreAudit(models.Model):
    """
    Store Front Status Log model.
    """
    store_front = models.ForeignKey("stores.StoreFront", on_delete=models.CASCADE)
    online = models.BooleanField()
    log_time = models.DateTimeField()

    def __str__(self):
        return "{} - {}".format(
            self.store_front,
            self.log_time.strftime("%c")
        )

    def save(self, *args, **kwargs):
        self.log_time = tz.localtime()
        super().save(*args, **kwargs)
        self.store_front.online = self.online
        self.store_front.save()
