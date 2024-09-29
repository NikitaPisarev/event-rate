from django.db import models


class Score(models.Model):
    event_id = models.CharField(max_length=255)
    score = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_final = models.BooleanField(default=False)

    def __str__(self):
        return f"Score {self.score} for event {self.event_id}"


class ScoreHistory(models.Model):
    score = models.ForeignKey(Score, on_delete=models.CASCADE, related_name="history")
    old_score = models.PositiveIntegerField()
    new_score = models.PositiveIntegerField()
    changed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Score {self.score} for event {self.score.event_id} (changed at {self.changed_at})"
