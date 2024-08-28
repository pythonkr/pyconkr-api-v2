from rest_framework import serializers


class PretalxSpeakerSerializer(serializers.Serializer):
    code = serializers.CharField()
    name = serializers.CharField()
    biography = serializers.CharField()
    avatar = serializers.CharField()


class PretalxSlotSerializer(serializers.Serializer):
    start = serializers.DateTimeField()
    end = serializers.DateTimeField()
    room = serializers.CharField()
    room_id = serializers.IntegerField()


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
    submission_type = serializers.CharField()
    submission_type_id = serializers.IntegerField()
    state = serializers.CharField()

    image = serializers.CharField()
    title = serializers.CharField()
    abstract = serializers.CharField()
    description = serializers.CharField()
    notes = serializers.CharField()
    internal_notes = serializers.CharField()
    content_locale = serializers.CharField()

    slot = PretalxSlotSerializer()
    duration = serializers.IntegerField()
    do_not_record = serializers.BooleanField()
    is_featured = serializers.BooleanField()

    speakers = PretalxSpeakerSerializer(many=True)
    answers = PretalxAnswerSerializer(many=True)

    tags = serializers.ListField()
    tag_ids = serializers.ListField()


class PretalxPaginatedSessionSerializer(serializers.Serializer):
    count = serializers.IntegerField()
    next = serializers.CharField()
    previous = serializers.CharField()
    results = PretalxSessionSerializer(many=True)
