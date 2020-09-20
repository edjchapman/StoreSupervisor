from django.utils import timezone as tz

from django.db import models


class Store(models.Model):
    """
    Store model
    """
    name = models.CharField(max_length=100)
    open_time = models.TimeField()
    close_time = models.TimeField()

    def __str__(self):
        return self.name


class StoreFront(models.Model):
    """
    Store Front model.
    """
    DELIVEROO = "DELIVEROO"
    UBER_EATS = "UBER_EATS"
    PLATFORM_CHOICES = [
        (DELIVEROO, "Deliveroo"),
        (UBER_EATS, "Uber Eats"),
    ]
    platform = models.CharField(max_length=100, choices=PLATFORM_CHOICES)
    url = models.URLField()
    store = models.ForeignKey("stores.Store", on_delete=models.CASCADE)
    online = models.BooleanField(default=False)

    class Meta:
        unique_together = ["store", "platform"]

    def __str__(self):
        return "{} - {}".format(
            self.store.name,
            self.get_platform_display()
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
