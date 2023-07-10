import datetime

from import_export import resources, fields
from import_export.widgets import ForeignKeyWidget

from session.models import Session, Category


class SessionResource(resources.ModelResource):
    def before_save_instance(self, instance: Session, using_transactions, dry_run):
        instance.start_at = datetime.datetime.now()

    class Meta:
        model = Session
        fields = ["id", "title", "difficulty", "duration", "language", "category"]
