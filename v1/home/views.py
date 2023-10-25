from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, CreateAPIView, ListAPIView
from rest_framework.permissions import IsAuthenticated
from v1.home.models import Board, Column, Task
from rest_framework.response import Response
from v1.home.serializers import BoardCreateSerializer, ColumnSerializer, TaskSerializer, ColumnCreateSerializer, \
    BoardGetDataSerializer, WorkerCreateSerializer, WorkerRedMessageSerializer
from rest_framework.views import APIView

from v1.services import send_message_email
from v1.user.models import User


# Create your views here.


class BoardCreateApi(ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = Board.objects.all()
    serializer_class = BoardCreateSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)


class BoardGetDataApi(ListAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = Board.objects.all()
    serializer_class = BoardGetDataSerializer

    def get_queryset(self):
        params = self.request.query_params
        board_id = params.get('board_id')
        board = self.queryset.filter(id=board_id).first()
        if not board:
            raise ValueError('Error')
        return board.board_columns.all()


class ColumnCreateApi(CreateAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = Task.objects.all()
    serializer_class = ColumnCreateSerializer


class BoardUpdateApi(RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = Board.objects.all()
    serializer_class = BoardCreateSerializer


class ColumnApi(RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = Column.objects.all()
    serializer_class = ColumnSerializer


class TaskCreateApi(ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = Task.objects.all()
    serializer_class = TaskSerializer


class TaskRUDApi(RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = Task.objects.all()
    serializer_class = TaskSerializer


class WorkerMessageCreateApi(CreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = WorkerCreateSerializer

    def perform_create(self, serializer):
        return serializer.save(inviter_id=self.request.user.id)


class WorkerCreateApi(CreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = WorkerRedMessageSerializer
