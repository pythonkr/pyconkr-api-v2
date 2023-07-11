from uuid import uuid4
from import_export.resources import ModelResource

from program.models import Program


class ProgramResource(ModelResource):
    def before_import_row(self, row, row_number=None, **kwargs):
        row["id"] = uuid4()

    def before_save_instance(self, instance: Program, using_transactions, dry_run):
        instance.id = uuid4()

    class Meta:
        model = Program
        fields = [
            "id",
            "host",
            "title",
            "short_desc",
            "desc",
            "room",
            "program_type"
        ]