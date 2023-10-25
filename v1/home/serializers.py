from rest_framework import serializers
from v1.home.models import Board, Column, Task, WorkerMessage, ActivWorker
from v1.user.models import WorkerCode
from django.db import transaction

from v1.services import send_message_email


class ColumnSerializer(serializers.ModelSerializer):
    class Meta:
        model = Column
        fields = ('id', 'title')


class ColumnCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Column
        fields = ('id', 'title', 'board')


class BoardGetDataSerializer(serializers.Serializer):
    columns = serializers.SerializerMethodField()
    tasks = serializers.SerializerMethodField()

    def get_columns(self, obj):
        return {
            'id': obj.id,
            'title': obj.title
        }

    def get_tasks(self, obj):
        return TaskGetSerializer(obj.column_task.all(), many=True).data

class ColumnDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Column
        fields = ("id", "title")

    def to_representation(self, instance):
        res = super().to_representation(instance)
        tasks = Task.objects.filter(column_id=instance.id)
        res['tasks'] = TaskSerializer(tasks, many=True).data
        return res

class BoardCreateSerializer(serializers.ModelSerializer):
    columns = serializers.ListField(write_only=True)

    class Meta:
        model = Board
        fields = ('id', 'title', 'description', 'columns')

    def create(self, validated_data):
        columns = validated_data.pop('columns')
        board = super().create(validated_data)
        # column_list = []
        # for column in columns:
        #     column_list.append(Column(title=column, board=board))
        # if column_list:
        #     Column.objects.bulk_create(column_list)
        with transaction.atomic():
            for column in columns:
                Column.objects.create(title=column, board=board)
        return board

    # def to_representation(self, instance):
    #     res = super().to_representation(instance)
    #     column = Column.objects.select_related('board').filter(board=instance)
    #     task = Task.objects.select_related('column').filter(column__board_id=instance.id)
    #     res['columns'] = ColumnSerializer(column, many=True).data
    #     res['tasks'] = TaskGetSerializer(task, many=True).data
    #     return res

    # def get_column(self, obj):
    #     column = Column.objects.select_related('board').filter(board=obj)
    #     return ColumnSerializer(column, many=True).data
    # def get_task(self, obj):
    #     task = Task.objects.select_related('column').filter(column__board_id=obj.id)
    #     return TaskGetSerializer(task, many=True).data

    def to_representation(self, instance):
        res = super().to_representation(instance)
        columns = Column.objects.select_related('board').filter(board=instance)
        res['columns'] = ColumnDetailSerializer(columns, many=True).data
        return res



class TaskGetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ('id', 'title', 'description')


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ('id', 'title', 'description', 'column')

    def validate(self, attrs):
        res = super().validate(attrs)
        column = res['column']
        user = self.context['request'].user
        if column.board.user.id != user.id:
            raise serializers.ValidationError('User')
        return res


class WorkerCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkerMessage
        fields = ('id', 'board', 'user')

    def validate(self, attrs):
        res = super().validate(attrs)
        board = res.get('board')
        if board.user != self.context['request'].user:
            raise serializers.ValidationError('Error')
        return res

    def create(self, validated_data):
        obj = super().create(validated_data)
        send_message_email(obj.user.email, obj.user)
        return obj


class WorkerRedMessageSerializer(serializers.ModelSerializer):
    code = serializers.CharField(write_only=True)

    class Meta:
        model = ActivWorker
        fields = ('id', 'board', 'inviter', 'code')

    def validate(self, attrs):
        res = super().validate(attrs)
        code1 = res.pop('code')
        user = WorkerCode.objects.filter(user=self.context['request'].user).first()
        code2 = user.worker_code
        if code2 != code1:
            raise serializers.ValidationError('Error code')
        WorkerMessage.objects.update(added=True)
        return res
