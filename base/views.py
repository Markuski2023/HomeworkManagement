from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from .models import Message, Group, Assignment, Subject
from .forms import SubjectForm

def home(request):

    subjects = Subject.objects.all()
    assignments = Assignment.objects.all()

    context = {'subjects': subjects, 'assignments': assignments}

    return render(request, 'base/home.html', context)

def subject(request, pk):
    subject = Subject.objects.get(id=pk)

    # if request.method == 'POST':
    #     note = Message.objects.create(
    #         user = request.user,
    #         room = room,
    #         body = request.POST.get('body')
    #     )
    #     return redirect('room', pk=room.id)

    context = {'subject': subject}
    return render(request, 'base/subject.html', context)


@login_required(login_url='login')
def createSubject(request):
    form = SubjectForm()

    if request.method == 'POST':

        Subject.objects.create(
            user = request.user,
            name = request.POST.get('name'),
        )
        return redirect('home')

    context = {'form': form}
    return render(request, 'base/subject_form.html', context)