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
    cover_image = models.ImageField(upload_to="project_covers/", null=True, blank=True)

    def __str__(self):
        return f"{self.title}"


class Contribution(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="contributions")
    donor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="contributions")
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.donor} → {self.project} ({self.amount})"
    