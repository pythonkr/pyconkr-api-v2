from rest_framework import serializers


class PretalxSpeakerSerializer(serializers.Serializer):
    code = serializers.CharField()
    name = serializers.CharField()
    biography = serializers.CharField(allow_null=True, allow_blank=True)
    avatar = serializers.CharField(allow_null=True, allow_blank=True)
    email = serializers.CharField()


class PretalxSlotSerializer(serializers.Serializer):
    start = serializers.DateTimeField(allow_null=True)
    end = serializers.DateTimeField(allow_null=True)
    room = serializers.DictField(allow_null=True)
    room_id = serializers.IntegerField(allow_null=True)


class PretalxQuestionSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    question = serializers.DictField()
    required = serializers.BooleanField()
    target = serializers.CharField()
    options = serializers.ListField()


class PretalxAnswerSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    question = PretalxQuestionSerializer()
    answer = serializers.CharField()
    answer_file = serializers.CharField()
    submission = serializers.CharField()
    person = serializers.CharField()
    options = serializers.ListField()


class PretalxSessionSerializer(serializers.Serializer):
    code = serializers.CharField()
    submission_type = serializers.DictField()
    submission_type_id = serializers.IntegerField()
    state = serializers.CharField()

    image = serializers.CharField(allow_null=True)
    title = serializers.CharField()
    abstract = serializers.CharField(allow_null=True)
    description = serializers.CharField(allow_null=True, allow_blank=True)
    notes = serializers.CharField(allow_null=True, allow_blank=True)
    internal_notes = serializers.CharField(allow_null=True, allow_blank=True)
    content_locale = serializers.CharField()

    slot = PretalxSlotSerializer(allow_null=True)
    duration = serializers.IntegerField(allow_null=True)
    do_not_record = serializers.BooleanField()
    is_featured = serializers.BooleanField()

    speakers = PretalxSpeakerSerializer(many=True)
    answers = PretalxAnswerSerializer(many=True)

    tags = serializers.ListField()
    tag_ids = serializers.ListField()


class PretalxPaginatedSessionSerializer(serializers.Serializer):
    count = serializers.IntegerField(allow_null=True)
    next = serializers.CharField(allow_null=True)
    previous = serializers.CharField(allow_null=True)
    results = PretalxSessionSerializer(many=True)
