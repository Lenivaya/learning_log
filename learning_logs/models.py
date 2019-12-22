from django.contrib.auth.models import User
from django.db import models


class Topic(models.Model):
    """Topic, that the user is exploring"""
    text = models.CharField(max_length=200)
    date_added = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(User, on_delete=models.PROTECT)

    def __str__(self):
        """Returns string representation of model"""
        return self.text


class Entry(models.Model):
    """Information about topic, that user has learned"""
    topic = models.ForeignKey(Topic, on_delete=models.PROTECT)
    text = models.TextField()
    data_added = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "entries"

    def __str__(self):
        """Returns string representation of model"""
        if len(self.text) > 50:
            return self.text[:50] + "..."
        else:
            return self.text
