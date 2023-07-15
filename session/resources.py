import datetime

from import_export import resources, fields
from import_export.widgets import ForeignKeyWidget

from session.models import Session, Category


class SessionResource(resources.ModelResource):
    def before_import_row(self, row, row_number=None, **kwargs):
        row["room_num"] = int(row["room_num"])

    class Meta:
        model = Session
        fields = ["id", "title", "difficulty", "duration", "language", "category", "start_at", "room_num"]
