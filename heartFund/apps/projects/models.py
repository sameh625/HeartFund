from django.db import models
from django.conf import settings

class Project(models.Model):
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete= models.CASCADE,
        related_name="projects"
    )
    title = models.CharField(max_length=200)
    details = models.TextField()
    target = models.DecimalField(max_digits=12, decimal_places=2)
    start_date = models.DateField()
    end_date = models.DateField()
    