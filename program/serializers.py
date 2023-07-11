from rest_framework import serializers

from program.models import Program


class ProgramSerializer(serializers.ModelSerializer):
    class Meta:
        model = Program
        fields = [
            "id",
            "host",
            "title",
            "short_desc",
            "desc",
            "room"
        ]
