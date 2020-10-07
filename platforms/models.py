from django.db import models


class Platform(models.Model):
    """
    Platform model.
    """
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

    def search_texts(self):
        return [i.search_text for i in self.offlinesearchtext_set.all()]


class OfflineSearchText(models.Model):
    """
    Offline Search Text model.
    """
    platform = models.ForeignKey('platforms.Platform', on_delete=models.CASCADE)
    search_text = models.CharField(max_length=100)

    def __str__(self):
        return self.search_text
