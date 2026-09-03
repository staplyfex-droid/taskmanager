from django.contrib.auth.forms import UserCreationForm
from django.forms import Form, EmailField, CharField, PasswordInput, Textarea, DateTimeInput, Select, ModelForm, TextInput, ChoiceField, EmailInput
from .models import Task
from django.contrib.auth.models import User

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

class EmailPasswordForm(Form):
    email = EmailField(
        label="Електронна пошта", 
        widget=EmailInput(attrs={
            'class': 'form-control-my form-control email',
            'placeholder': 'Ваша пошта',
            'style': 'background-color: #f7decdeb;'
        })
    )
    password = CharField(
        widget=PasswordInput(attrs={
            'class': 'form-control-my form-control email',
            'placeholder': 'Пароль',
            'style': 'background-color: #f7decdeb;'
        }),
        label="Пароль"
    )

class UserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]
        widgets = {
            "username": TextInput(attrs={
                'class': 'form-control-my form-control email',
                'placeholder': 'Імя користувача',
                'style': 'background-color: #f7decdeb; '
            }),
            "email": EmailInput(attrs={
                'class': 'form-control-my form-control email',
                'placeholder': 'Ваша пошта',
                'style': 'background-color: #f7decdeb;'
            }),
            "password1": PasswordInput(attrs={
                'class': 'form-control-my form-control',
                'placeholder': 'Придумайте пароль',
            }),
            "password2": PasswordInput(attrs={
                'class': 'form-control-my form-control',
                'placeholder': 'Повторіть пароль'
            })
        }

