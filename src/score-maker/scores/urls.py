from django.urls import path

from scores.views import get_scores_history, set_score
from scores.monitoring import health_check

urlpatterns = [
    path('set-score/', set_score),
    path('scores/', get_scores_history),
    path('health/', health_check),
]
