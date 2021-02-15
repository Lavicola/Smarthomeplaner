from django.db import models

# Create your models here.

class FundamentalsEntry(models.Model):
    title = models.CharField(max_length=70)
    text = models.CharField(max_length=65000)

    def __str__(self):
        return self.title
