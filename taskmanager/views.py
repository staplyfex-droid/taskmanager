from django.shortcuts import render
from django.views.generic import ListView, UpdateView, DeleteView
from taskmanager import models
from django.urls import reverse_lazy
from .forms import TaskForm, FilterForm 
from django.contrib.auth.mixins import LoginRequiredMixin
from .mixins import UserIsOwnerMixin
from django.db.models import Q

class TaskListView(ListView):
    model = models.Task
    template_name = 'taskmanager/task_list.html'
    context_object_name = 'tasks'
    def get_queryset(self):
        queryset = super().get_queryset()
        status = self.request.GET.get('status', '')
        priority = self.request.GET.get('priority', '')
        user = self.request.user
        try:
            executor = models.Executor.objects.get(executor_id=user.id)
        except: executor = None
        if user.is_authenticated:
            if executor:
                queryset = queryset.filter(Q(created_by__username=user)| Q(executors=executor))
            else:
                queryset = queryset.filter(created_by__username=user)
        if status:
            queryset = queryset.filter(status=status)
        if priority:
            queryset = queryset.filter(priority=priority)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        if user.is_authenticated:
            executors = models.Executor.objects.filter(executor_id = user.id)
        else:
            executors = models.Executor.objects.none()
        context['executors_t'] = executors
        context['form'] = FilterForm(self.request.GET)
        return context

     
class UpdateTaskView(LoginRequiredMixin, UserIsOwnerMixin, UpdateView):
    model = models.Task
    form_class = TaskForm
    template_name = 'taskmanager/task_update.html'
    success_url = reverse_lazy('task_list')

class DeleteTaskView(LoginRequiredMixin, UserIsOwnerMixin, DeleteView):
    model = models.Task
    template_name = 'taskmanager/task_confirm_delete.html'
    success_url = reverse_lazy('task_list')

