from rest_framework import serializers

from scores.models import ScoreHistory


class ScoreHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ScoreHistory
        fields = ['event_id', 'old_score', 'new_score', 'changed_at']
