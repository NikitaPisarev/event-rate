from rest_framework import serializers

from scores.models import ScoreHistory


class ScoreHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ScoreHistory
        fields = ['event_id', 'old_score', 'new_score']

    def validate_new_score(self, value: int) -> int:
        if not 1 <= value <= 5:
            raise serializers.ValidationError("Score must be between 1 and 5.")
        return
