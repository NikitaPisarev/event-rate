from adrf.decorators import api_view
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import status
from asgiref.sync import sync_to_async

from scores.models import ScoreHistory
from scores.serializers import ScoreHistorySerializer
from scores.services import fetch_event, is_event_within_deadline, send_score_to_kafka


@api_view(["GET"])
async def get_scores_history(request: Request) -> Response:
    scores = await sync_to_async(list)(ScoreHistory.objects.all())
    serializer = ScoreHistorySerializer(scores, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(["POST"])
async def set_score(request: Request) -> Response:
    event_id = request.data.get("event_id")
    new_score = request.data.get("score")

    event = await fetch_event(event_id)
    if not event:
        return Response(
            {"error": "Event not found."},
            status=status.HTTP_403_FORBIDDEN,
        )

    if not await is_event_within_deadline(event):
        return Response(
            {"error": "The deadline for the event is over."},
            status=status.HTTP_403_FORBIDDEN,
        )

    old_score = await get_old_score(event_id)

    if old_score is not None and old_score == new_score:
        return Response(
            {"error": "New score is the same as the old score"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    score_data = {
        "event_id": event_id,
        "old_score": None,
        "new_score": new_score,
    }

    serializer = ScoreHistorySerializer(data=score_data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    await save_score_history(event_id, old_score, new_score)

    await send_score_to_kafka(event_id, new_score)
    return Response(
        {"event_id": event_id, "score": new_score}, status=status.HTTP_201_CREATED
    )


@sync_to_async
def get_old_score(event_id: str) -> int | None:
    last_score = (
        ScoreHistory.objects.filter(event_id=event_id).order_by("-changed_at").first()
    )
    return last_score.new_score if last_score else None


@sync_to_async
def save_score_history(event_id: str, old_score: int | None, new_score: int) -> None:
    ScoreHistory.objects.create(
        event_id=event_id, old_score=old_score, new_score=new_score
    )
