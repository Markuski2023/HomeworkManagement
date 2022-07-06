from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm


from .models import Subject, Assignment, User

# class UserForm(UserCreationForm):
#     class Meta:
#         model = User
#         fields = '__all__'

class SubjectForm(ModelForm):
    class Meta:
        model = Subject
        fields = '__all__'
        exclude = ['user']

class AssignmentForm(ModelForm):
    class Meta:
        model = Assignment
        fields =['name', 'body', 'due_date']
        exclude = ['user', 'grade']