from django.urls import path
from v1.home.views import (BoardCreateApi, BoardUpdateApi, ColumnApi, TaskCreateApi,
                           TaskRUDApi, ColumnCreateApi, BoardGetDataApi, WorkerMessageCreateApi,
                           WorkerCreateApi)

urlpatterns = [
    path('real/worker/', WorkerCreateApi.as_view()),
    path('worker/', WorkerMessageCreateApi.as_view()),
    path('board/get/', BoardGetDataApi.as_view()),
    path('column/create/', ColumnCreateApi.as_view()),
    path('board/create/', BoardCreateApi.as_view()),
    path('board/update/<int:pk>/', BoardUpdateApi.as_view()),
    path('column/update/<int:pk>/', ColumnApi.as_view()),
    path('task/create/', TaskCreateApi.as_view()),
    path('task/rud/<int:pk>/', TaskRUDApi.as_view()),
]
