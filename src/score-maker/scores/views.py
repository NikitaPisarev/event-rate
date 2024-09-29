from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import status
from asgiref.sync import sync_to_async

from scores.models import Score, ScoreHistory
from scores.serializers import ScoreHistorySerializer, ScoreSerializer


@api_view(['GET'])
async def get_scores(request: Request) -> Response:
    scores = await sync_to_async(list)(Score.objects.all())
    serializer = ScoreSerializer(scores, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
async def get_scores_history(request: Request) -> Response:
    scores = await sync_to_async(list)(ScoreHistory.objects.all())
    serializer = ScoreHistorySerializer(scores, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
async def set_score(request: Request) -> Response:
    event_id = request.data.get('event_id')
    new_score = request.data.get('score')

    score = get_score_by_event_id(event_id)
    if score:
        old_score = score.score
        score.score = new_score
        await save_score(score)
        await save_score_history(score, old_score, new_score)
    else:
        score = await create_score(event_id, new_score)

    serializer = ScoreSerializer(score)
    return Response(serializer.data, status=status.HTTP_201_CREATED)


@sync_to_async
def get_score_by_event_id(event_id: str) -> Score:
    try:
        return Score.objects.get(event_id=event_id)
    except Score.DoesNotExist:
        return None


@sync_to_async
def create_score(event_id: str, score: int) -> Score:
    return Score.objects.create(event_id=event_id, score=score)


@sync_to_async
def save_score(score: Score) -> None:
    score.save()


@sync_to_async
def save_score_history(score: Score, old_score: int, new_score: int) -> None:
    ScoreHistory.objects.create(score=score, old_score=old_score, new_score=new_score)
