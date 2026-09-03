from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, UpdateView, DeleteView, View, DetailView, CreateView
from taskmanager import models
from django.urls import reverse_lazy
from .forms import TaskForm, FilterForm, EmailPasswordForm, UserForm
from django.contrib.auth.mixins import LoginRequiredMixin
from .mixins import UserIsOwnerMixin
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.contrib.auth import logout, login
from django.contrib import messages
from django.contrib.auth.models import User
from django.db import IntegrityError


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

class CompliteView(LoginRequiredMixin, UserIsOwnerMixin, View):
    def post(self, request, *args, **kwargs):
        task = self.get_object()
        task.status = 'done'
        task.save()
        return HttpResponseRedirect(reverse_lazy('task_list'))
    def get_object(self):
        task_id = self.kwargs.get('pk')
        return get_object_or_404(models.Task, pk = task_id)
    
class UprovedTaskView(View):
    def post(self, request):
        executor_id = request.POST.get('executor_id')
        if executor_id:
            executor = models.Executor.objects.get(id=executor_id, executor_id=request.user)
            executor.approved = True
            executor.save()
        return redirect('task_list')

class TaskListDetailView(LoginRequiredMixin, UserIsOwnerMixin, DetailView):
    model = models.Task
    template_name = 'taskmanager/task_detail.html'
    context_object_name = 'task_detail'
    def get_queryset(self):
        queryset = super().get_queryset()
        user = self.request.user
        executor = models.Executor.objects.filter(executor_id= user.id).first()
        if user.is_authenticated:
            queryset = queryset.filter(Q(created_by__username=user)| Q(executors=executor))
        return queryset
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        task = self.get_object()
        user = self.request.user
        context['is_executor'] = task.executors.filter(executor_id=user).exists()
        return context
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        task = self.object
        new_status = request.POST.get('status')
        if new_status in dict(task.STATUS_CHOISES):
            task.status = new_status
            task.save()
            return redirect('task_detail', pk=task.pk)
    
def logout_view(request):
    logout(request)
    return redirect('task_list')

def request_login(request):
    if request.method == 'POST':
        form = EmailPasswordForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']

            # Перевірка користувача
            try:
                admin = User.objects.get(email=email)
                if admin.check_password(password):
                    login(request, admin)
                    request.session['username'] = admin.username
                    messages.success(request, 'Ви успішно увійшли як адмін!')
                    return redirect('task_list')
                else:
                    messages.error(request, 'Невірний пароль!')
                    return redirect('login')
            except User.DoesNotExist:
                messages.error(request, 'Користувач або адмін з таким email не знайдено.')
                return redirect('login')

    else:
        form = EmailPasswordForm()
    return render(request, 'todo/request_login.html', {'form': form})

def add_user(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            try:
                user = form.save()
                request.session['username'] = user.username
                messages.success(request, 'Користувач успішно створений!')
                return redirect('task_list')
            except IntegrityError:
                messages.error(request, 'Користувач з такою поштою вже зареєстрований.')
        else:
            print(form.errors)
            messages.error(request, 'Виникла помилка. Перевірте введені дані.')
    else:
        form = UserForm()
    
    return render(request, 'taskmanager/create_user.html', {'form': form})

class CreateTaskView(LoginRequiredMixin, CreateView):
    model = models.Task
    template_name = 'taskmanager/create_task.html'
    form_class = TaskForm
    success_url = reverse_lazy('task_list')
    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)
