from django.contrib import admin
from .models import Project

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ("title", "owner", "target", "start_date", "end_date")
    search_fields = ("title", "details")
    list_filter = ("start_date", "end_date")
