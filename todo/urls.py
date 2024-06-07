from django.urls import path, include
from .views import TaskList, TaskDetail, TaskCreate, TaskDelete, TaskUpdate

urlpatterns = [
    path('list/', TaskList.as_view(), name='list'),
    path('detail/<int:pk>', TaskDetail.as_view(), name='detail'),
    path('create/', TaskCreate.as_view(), name='create'),
    path('delete/<int:pk>', TaskDelete.as_view(), name='delete'),
    path('update/<int:pk>', TaskUpdate.as_view(), name='update')
]
