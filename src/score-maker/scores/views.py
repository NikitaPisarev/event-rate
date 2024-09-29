from adrf.decorators import api_view
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import status
from asgiref.sync import sync_to_async

from scores.models import ScoreHistory
from scores.serializers import ScoreHistorySerializer
from scores.services import is_event_within_deadline, send_score_to_kafka


@api_view(['GET'])
async def get_scores_history(request: Request) -> Response:
    scores = await sync_to_async(list)(ScoreHistory.objects.all())
    serializer = ScoreHistorySerializer(scores, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
async def set_score(request: Request) -> Response:
    event_id = request.data.get('event_id')
    new_score = request.data.get('score')

    if not await is_event_within_deadline(event_id):
        return Response({'error': 'Event not found or not within deadline'}, status=status.HTTP_403_FORBIDDEN)

    # old_score = await get_score_by_event_id(event_id)
    await save_score_history(event_id, 1, new_score)  # TODO: add old_score

    await send_score_to_kafka(event_id, new_score)
    return Response({'event_id': event_id, 'score': new_score}, status=status.HTTP_201_CREATED)


@sync_to_async
def save_score_history(event_id: str, old_score: int | None, new_score: int) -> None:
    ScoreHistory.objects.create(event_id=event_id, old_score=old_score, new_score=new_score)
