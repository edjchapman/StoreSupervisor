from django.db import models
from django.utils import timezone as tz, timezone


class OpeningTimes(models.Model):
    """
    Store Opening Times model.
    """
    open_time = models.TimeField()
    close_time = models.TimeField()
    monday = models.BooleanField(default=True)
    tuesday = models.BooleanField(default=True)
    wednesday = models.BooleanField(default=True)
    thursday = models.BooleanField(default=True)
    friday = models.BooleanField(default=True)
    saturday = models.BooleanField(default=True)
    sunday = models.BooleanField(default=True)

    class Meta:
        abstract = True


class Store(OpeningTimes):
    """
    Store model
    """
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    def open_today(self):
        day_dict = {
            0: "monday",
            1: "tuesday",
            2: "wednesday",
            3: "thursday",
            4: "friday",
            5: "saturday",
            6: "sunday",
        }
        day = timezone.localtime().day
        return getattr(self, day_dict[day])

    def open_now(self):
        now = timezone.localtime().time()
        if self.open_time > self.close_time:  # e.g. 12:00 - 06:00
            if now > self.open_time or now < self.close_time:
                return True
        elif self.open_time < self.close_time:  # e.g. 06:00 - 24:00
            if self.open_time < now < self.close_time:
                return True
        elif self.open_time == self.close_time:  # 24 Hours
            return True


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


class StoreFrontStatusLog(models.Model):
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
