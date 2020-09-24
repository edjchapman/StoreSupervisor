from django.db import models


class Platform(models.Model):
    """
    Platform model.
    """
    name = models.CharField(max_length=100, unique=True)
    offline_search_text = models.CharField(
        max_length=100,
        help_text="Text to search on a store front page to see if it is offline."
    )

    def __str__(self):
        return self.name
