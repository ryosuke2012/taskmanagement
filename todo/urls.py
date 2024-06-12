from django.urls import path, include
from . import views
urlpatterns = [
    path('list/', views.TaskList, name='list'),
    path('detail/<int:pk>', views.TaskDetail, name='detail'),
    path('create/', views.TaskCreate, name='create'),
    path('delete/<int:pk>', views.TaskDelete, name='delete'),
    path('update/<int:pk>', views.TaskUpdate, name='update')
]
