from rest_framework import serializers

from apps.core.models import Answer, Poll, Question, UserChoice


class PollListSerializer(serializers.ModelSerializer):
    # not_started / in_progress / completed, считается аннотацией во вьюхе
    status = serializers.CharField(read_only=True)

    class Meta:
        model = Poll
        fields = ("id", "title", "status")


class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = ("id", "title", "is_open_answer")


class QuestionSerializer(serializers.ModelSerializer):
    answers = AnswerSerializer(many=True, read_only=True)

    class Meta:
        model = Question
        fields = ("id", "title", "answers")


class NextQuestionSerializer(serializers.Serializer):
    completed = serializers.BooleanField()
    answered = serializers.IntegerField()
    total = serializers.IntegerField()
    question = QuestionSerializer(allow_null=True)


class UserChoicePostSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserChoice
        fields = ("answer", "answer_text")
        extra_kwargs = {"answer_text": {"allow_blank": False}}

    def validate(self, attrs):
        if attrs["answer"].is_open_answer:
            if not attrs.get("answer_text"):
                raise serializers.ValidationError({"answer_text": "Для ответа нужно передать его текст"})
        else:
            # тут важное, мы не хотим плодить текстовые поля в огромной таблице, поэтому превращаем в None
            attrs["answer_text"] = None

        return attrs

