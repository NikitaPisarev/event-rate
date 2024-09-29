from django.db import models


class ScoreHistory(models.Model):
    event_id = models.CharField(max_length=24)
    old_score = models.PositiveIntegerField()
    new_score = models.PositiveIntegerField()
    changed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Score {self.new_score} for event {self.event_id} (changed at {self.changed_at})"
