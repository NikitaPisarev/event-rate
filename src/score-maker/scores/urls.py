from django.urls import path

from scores.views import get_scores_history, set_score

urlpatterns = [
    path('set-score/', set_score),
    path('scores-history/', get_scores_history),
]
