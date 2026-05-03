from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .models import Task
from .forms import TaskForm

@login_required
def task_list(request):
    if request.user.is_superuser:
        tasks = Task.objects.all()
    else:
        tasks = Task.objects.filter(responsable=request.user)
        
    statut = request.GET.get('statut')
    recherche = request.GET.get('recherche')
    
    if statut:
        tasks = tasks.filter(statut=statut)
    if recherche:
        tasks = tasks.filter(titre__icontains=recherche)

    now = timezone.now()
    for task in tasks:
        task.is_past_due = False
        task.is_near_due = False
        if task.date_limite:
            if task.date_limite < now:
                task.is_past_due = True
            elif (task.date_limite - now).days <= 2:
                task.is_near_due = True

    return render(request, 'tasks/task_list.html', {'tasks': tasks})

@login_required
def task_create(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.responsable = request.user
            task.save()
            return redirect('task_list')
    else:
        form = TaskForm()
    return render(request, 'tasks/task_form.html', {'form': form})

@login_required
def task_update(request, pk):
    task = get_object_or_404(Task, pk=pk)
    if task.responsable != request.user and not request.user.is_superuser:
        return redirect('task_list')
        
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('task_list')
    else:
        form = TaskForm(instance=task)
    return render(request, 'tasks/task_form.html', {'form': form})

@login_required
def task_delete(request, pk):
    task = get_object_or_404(Task, pk=pk)
    if task.responsable != request.user and not request.user.is_superuser:
        return redirect('task_list')

    if request.method == 'POST':
        task.delete()
        return redirect('task_list')
    return render(request, 'tasks/task_confirm_delete.html', {'task': task})

from django.contrib.auth import login
from .models import ResponsableProfile
from .forms import CustomUserCreationForm

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            ResponsableProfile.objects.create(user=user, service="Non assigné")
            login(request, user)
            return redirect('task_list')
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/register.html', {'form': form})