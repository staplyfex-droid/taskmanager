from django.db import models
from django.contrib.auth.models import User


class Task(models.Model):
    STATUS_CHOISES = [
        ('todo', 'Зробити'),
        ('in_process', 'В процесі'),
        ('done', 'Завершено')
    ]
    PRIORITY_CHOISES = [
        ('Low', 'Маленький'),
        ('medium', 'Середній'),
        ('High', 'Великий')
    ]
    title = models.CharField(max_length=150)
    description = models.TextField(null=True, blank=True)
    status = models.CharField(max_length=20, default= 'todo', choices=STATUS_CHOISES)
    priority = models.CharField(max_length=20, default= 'medium', choices=PRIORITY_CHOISES)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tasks')
    deadline = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

class Executor(models.Model):
    task_id = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='executors')
    executor_id = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    approved = models.BooleanField(default=False)

class Comment(models.Model):
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField(max_length=300,verbose_name='Введіть коментар')
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f'Comment by {self.creator.username} on {self.task.title}'




