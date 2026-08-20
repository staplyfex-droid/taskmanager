from django.shortcuts import render
from django.views.generic import ListView
from taskmanager import models

class TaskListView(ListView):
    model = models.Task
    template_name = 'taskmanager/task_list.html'
    context_object_name = 'tasks'
     

