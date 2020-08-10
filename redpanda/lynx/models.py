from hashlib import md5

from django.db import models


class URL(models.Model):
    earl_full = models.URLField(max_length=768)
    earl_hash = models.URLField(max_length=200, unique=True)
    clicks = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def clicked(self):
        self.clicks += 1
        self.save()

    def save(self, *args, **kwargs):
        if not self.id:
            self.earl_hash = md5(self.earl_full.encode()).hexdigest()[:10]

        return super().save(*args, **kwargs)
