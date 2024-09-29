from django.urls import path

from scores.views import get_scores, get_scores_history, set_score

urlpatterns = [
    path('scores/', get_scores),
    path('set-score/', set_score),
    path('scores-history/', get_scores_history),
]
