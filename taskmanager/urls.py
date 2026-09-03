from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.TaskListView.as_view(), name='task_list'),
    path('task_detail-<int:pk>/', views.TaskListDetailView.as_view(), name='task_detail'),
    path('new_task', views.CreateTaskView.as_view(), name='new_task'),
    path('<int:pk>/complete', views.CompliteView.as_view(), name='complete_task'),
    path('task_update/<int:pk>/', views.UpdateTaskView.as_view(), name='task_update'),
    path('task_delete/<int:pk>/', views.DeleteTaskView.as_view(), name='task_delete'),
    path('approve_task/', views.UprovedTaskView.as_view(), name='approve_task'),
    path('logout/', views.logout_view, name='logout'),
    path('login/', views.request_login, name='login'),
    path('add_user/', views.add_user, name='add_user'),
]