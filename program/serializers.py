from rest_framework import serializers

from program.models import Program


class ProgramSerializer(serializers.ModelSerializer):
    class Meta:
        model = Program
        fields = [
            "id",
            "host",
            "profile_img",
            "title",
            "short_desc",
            "desc",
            "room",
            "start_at",
            "end_at",
        ]
