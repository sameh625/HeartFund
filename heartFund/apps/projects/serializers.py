from rest_framework import serializers
from .models import Project

class ProjectSerializer(serializers.ModelSerializer):
    owner = serializers.SerializerMethodField()
    payment_info = serializers.CharField(source="owner.payment_info", read_only=True)

    class Meta:
        model = Project
        fields = ["id","title","details","target","start_date","end_date","owner","payment_info"]
        read_only_fields = ["id", "current_amount", "owner"]

    def get_owner(self, obj):
        return f"{obj.owner.first_name}"