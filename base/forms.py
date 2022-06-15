from django.forms import ModelForm

from .models import Subject, User

class SubjectForm(ModelForm):
    class Meta:
        model = Subject
        fields = '__all__'
        exclude = ['user']