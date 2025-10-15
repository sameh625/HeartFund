from decimal import Decimal
from django.db import models
from rest_framework import serializers
from .models import Project, Contribution

class ProjectSerializer(serializers.ModelSerializer):
    owner = serializers.SerializerMethodField()
    cover_image_url = serializers.SerializerMethodField(read_only=True)
    current_amount = serializers.SerializerMethodField(read_only=True)
    progress_percent = serializers.SerializerMethodField(read_only=True)
    is_fully_funded = serializers.SerializerMethodField(read_only=True)
    can_donate = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Project
        fields = [
            "id",
            "title",
            "details",
            "target",
            "start_date",
            "end_date",
            "owner",
            "cover_image",
            "cover_image_url",
            "current_amount",
            "progress_percent",
            "is_fully_funded",
            "can_donate",
        ]
        read_only_fields = ["id", "owner"]

    def get_owner(self, obj):
        return f"{obj.owner.first_name}"

    def get_cover_image_url(self, obj):
        if obj.cover_image:
            request = self.context.get("request")
            url = obj.cover_image.url
            return request.build_absolute_uri(url) if request else url
        return None

    def get_current_amount(self, obj):
        total = obj.contributions.aggregate(total_amount=models.Sum("amount")).get("total_amount")
        return str(total or Decimal("0"))

    def get_progress_percent(self, obj):
        try:
            target = Decimal(str(obj.target))
            current = Decimal(self.get_current_amount(obj))
            if target > 0:
                percent = (current / target) * Decimal("100")
                if percent > 100:
                    percent = Decimal("100")
                return float(round(percent, 2))
        except Exception:
            return 0.0
        return 0.0

    def get_is_fully_funded(self, obj):
        try:
            target = Decimal(str(obj.target))
            current = Decimal(self.get_current_amount(obj))
            return current >= target and target > 0
        except Exception:
            return False

    def get_can_donate(self, obj):
        request = self.context.get("request")
        if request and getattr(request, "user", None) and request.user.is_authenticated:
            if obj.owner_id == request.user.id:
                return False
        return not self.get_is_fully_funded(obj)


class ContributionSerializer(serializers.ModelSerializer):
    donor_name = serializers.SerializerMethodField()

    class Meta:
        model = Contribution
        fields = ["id", "donor_name", "amount", "created_at"]
        read_only_fields = ["id", "donor_name", "created_at"]

    def get_donor_name(self, obj):
        return obj.donor.first_name