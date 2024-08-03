from django.db import models

class Person(models.Model):
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    country = models.CharField(max_length=100)

    def __str__(self):
        return self.name