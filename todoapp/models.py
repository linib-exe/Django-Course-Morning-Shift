from django.db import models

# Create your models here.
class TODO(models.Model):
    title = models.CharField(max_length=20)
    description = models.TextField()
    is_done = models.BooleanField()

    def __str__(self):
        return self.title