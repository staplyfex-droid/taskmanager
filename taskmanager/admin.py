from django.contrib import admin
from .models import Task, Executor, Comment

admin.site.register(Task)
admin.site.register(Executor)
admin.site.register(Comment)
