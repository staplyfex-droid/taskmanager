from django.contrib.auth.forms import UserCreationForm
from django.forms import Form, EmailField, CharField, PasswordInput, Textarea, DateTimeInput, Select, ModelForm, TextInput, ChoiceField
from .models import Task

class FilterForm(Form):
    STATUS_CHOISES = [
        ('', 'Всі'),
        ('todo', 'Зробити'),
        ('in_process', 'В процесі'),
        ('done', 'Завершено')
    ]
    PRIORITY_CHOISES = [
        ('', 'Всі'),
        ('Low', 'Маленький'),
        ('Medium', 'Середній'),
        ('High', 'Великий')
    ]
    status = ChoiceField(
        choices=STATUS_CHOISES,
        required=False,
        label='Статус',
        widget=Select(attrs={'class': 'form-control'})
    )
    priority = ChoiceField(
        choices=PRIORITY_CHOISES,
        required=False,
        label='Пріоритет',
        widget=Select(attrs={'class': 'form-control'})
    )

class TaskForm(ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'status', 'priority', 'executor', 'deadline']
        widgets = {
            'title': TextInput(attrs={'class': 'form-control', 'placeholder':'Назва Завдання'}),
            'description': Textarea(attrs={'class': 'form-control', 'placeholder':'Опис Завдання'}),
            'status': Select(attrs={'class': 'form-control'}),
            'priority': Select(attrs={'class': 'form-control'}),
            'executor': Select(attrs={'class': 'form-control'}),
            'deadline': DateTimeInput(attrs={'type':'datetime-local', 'placeholder': 'Дата кінця'})
        }