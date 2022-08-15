from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

from .models import Message, Group, Assignment, Subject, Note
# User
from .forms import SubjectForm, AssignmentForm
# UserCreationForm

def loginPage(request):

    page = 'login'

    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'User not found...')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Username or password incorrect...')

    context = {'page': page}
    return render(request, 'base/login_register.html', context)

def registerPage(request):
    form = UserCreationForm()

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'An error has occurred. Please try again..')

    return render(request, 'base/login_register.html', {'form': form})

def logoutUser(request):
    logout(request)
    return redirect('loginPage')

@login_required(login_url='loginPage')
def home(request):

    now = timezone.now()
    upcoming = []

    subjects = Subject.objects.all()
    assignments = Assignment.objects.order_by('due_date')

    for i in assignments:
        if i.due_date >= now:
            upcoming.append(i)

    context = {'subjects': subjects, 'previous': upcoming}

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
            due_date = request.POST.get('due_date'),
        )
        return redirect('subject', pk=subject.id)

    context = {'form': form, 'subject': subject}
    return render(request, 'base/assignment_form.html', context)

@login_required(login_url='login')
def deleteSubject(request, pk):
    subject = Subject.objects.get(id=pk)

    if request.method == 'POST':
        subject.delete()
        return redirect('home')
    return render(request, 'base/delete.html', {'obj': subject})

@login_required(login_url='login')
def deleteAssignment(request, pk):
    assignment = Assignment.objects.get(id=pk)
    subject = assignment.subject.id

    if request.method == 'POST':
        assignment.delete()
        return redirect('subject', pk=subject)

    context = {'obj': assignment, 'subject': subject}

    return render(request, 'base/delete.html', context)

@login_required(login_url='login')
def deleteNote(request, pk):
    note = Note.objects.get(id=pk)
    subject = note.subject.id

    if request.method == 'POST':
        note.delete()
        return redirect('subject', pk=subject)

    context = {'obj': note, 'subject': subject}

    return render(request, 'base/delete.html', context)

@login_required(login_url='login')
def updateSubject(request, pk):
    subject = Subject.objects.get(id=pk)
    form = SubjectForm(instance=subject)

    if request.user != subject.user:
        return HttpResponse('Youre not allowed here')

    if request.method == 'POST':
        subject.name = request.POST.get('name')

        subject.save()

        return redirect('home')

    context = {'form': form, 'subject': subject}
    return render(request, 'base/subject_form.html', context)

@login_required(login_url='login')
def updateAssignment(request, pk):
    assignment = Assignment.objects.get(id=pk)
    subject = assignment.subject

    form = AssignmentForm(instance=assignment)

    if request.method == 'POST':
        assignment.name = request.POST.get('name')
        assignment.body = request.POST.get('body')
        assignment.due_date = request.POST.get('due_date')

        assignment.save()

        return redirect('subject', pk=subject.id)

    context = {'form': form, 'assignment': assignment, 'subject': subject}
    return render(request, 'base/assignment_form.html', context)

def grades(request):
    return render(request, 'base/grades.html')

@login_required(login_url='login')
def groups(request):

    groups = Group.objects.all()

    context = {'groups': groups}

    return render(request, 'base/groups.html', context)

@login_required(login_url='login')
def createGroup(request):
    form = SubjectForm()

    if request.method == 'POST':

        Subject.objects.create(
            user = request.user,
            name = request.POST.get('name'),
        )
        return redirect('home')

    context = {'form': form}
    return render(request, 'base/group_form.html', context)