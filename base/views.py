from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone

from .models import Message, Group, Assignment, Subject, Note
from .forms import SubjectForm, AssignmentForm

def home(request):

    subjects = Subject.objects.all()
    assignments = Assignment.objects.all()

    context = {'subjects': subjects, 'assignments': assignments}

    return render(request, 'base/home.html', context)

def subject(request, pk):

    now = timezone.now()

    subject = Subject.objects.get(id=pk)
    subject_notes = subject.note_set.all().order_by('created')
    assignments = Assignment.objects.all()
    assignments_sorted = Assignment.objects.order_by('due_date')

    previous = []
    upcoming = []

    for i in assignments:
        if i.due_date < now:
            previous.append(i)

    for i in assignments_sorted:
        if i.due_date >= now:
            upcoming.append(i)

    if request.method == 'POST':
        note = Note.objects.create(
            user = request.user,
            subject = subject,
            body = request.POST.get('body')
        )
        return redirect('subject', pk=subject.id)

    context = {'subject': subject, 'subject_notes': subject_notes,
               'assignments': assignments, 'previous': previous, 'upcoming': upcoming}
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

@login_required(login_url='login')
def createAssignment(request, pk):
    form = AssignmentForm()
    subject = Subject.objects.get(id=pk)

    if request.method == 'POST':
        Assignment.objects.create(
            subject=subject,
            name = request.POST.get('name'),
            body = request.POST.get('body'),
            due_date = timezone.now()
        )
        return redirect('subject', pk=subject.id)

    context = {'form': form, 'subject': subject}
    return render(request, 'base/assignment_form.html', context)