from rest_framework import serializers

from scores.models import Score, ScoreHistory


class ScoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Score
        fields = ['id', 'event_id', 'score', 'created_at', 'is_final']


class ScoreHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ScoreHistory
        fields = ['event_id', 'old_score', 'new_score', 'changed_at']
