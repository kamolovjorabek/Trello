from django.db import models
# Create your models here.


class DefaultAbstract(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Board(DefaultAbstract):
    title = models.CharField(max_length=255)
    description = models.TextField()
    user = models.ForeignKey('user.User', on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class Column(DefaultAbstract):
    title = models.CharField(max_length=255)
    board = models.ForeignKey(Board, on_delete=models.CASCADE, related_name='board_columns')

    def __str__(self):
        return self.title


class Task(DefaultAbstract):
    title = models.CharField(max_length=255)
    description = models.TextField()
    column = models.ForeignKey(Column, on_delete=models.CASCADE, related_name='column_task')

    def __str__(self):
        return f"{self.column} -> {self.title}"


class WorkerMessage(DefaultAbstract):
    user = models.ForeignKey('user.User', on_delete=models.CASCADE, related_name='user')
    board = models.ForeignKey(Board, on_delete=models.CASCADE)
    inviter = models.ForeignKey('user.User', on_delete=models.CASCADE, related_name='inviter')
    added = models.BooleanField(default=False)

    class Meta:
        unique_together = ('user', 'board')


class ActivWorker(DefaultAbstract):
    board = models.ForeignKey(Board, on_delete=models.CASCADE)
    inviter = models.ForeignKey('user.User', on_delete=models.CASCADE, related_name='inviter_worker')

    class Meta:
        unique_together = ('board',)
