from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta
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
    date_filtre = request.GET.get('date_filtre')
    responsable_id = request.GET.get('responsable')
    
    if statut:
        tasks = tasks.filter(statut=statut)
    if recherche:
        tasks = tasks.filter(titre__icontains=recherche)

    # Filtre par date limite
    now = timezone.now()
    if date_filtre == 'depassee':
        tasks = tasks.filter(date_limite__lt=now)
    elif date_filtre == 'aujourd_hui':
        tasks = tasks.filter(date_limite__date=now.date())
    elif date_filtre == 'semaine':
        tasks = tasks.filter(date_limite__lte=now + timedelta(days=7), date_limite__gte=now)
    elif date_filtre == 'mois':
        tasks = tasks.filter(date_limite__lte=now + timedelta(days=30), date_limite__gte=now)

    # Filtre par responsable (admin seulement)
    if request.user.is_superuser and responsable_id:
        tasks = tasks.filter(responsable_id=responsable_id)

    # Indicateurs visuels
    for task in tasks:
        task.is_past_due = False
        task.is_near_due = False
        if task.date_limite:
            if task.date_limite < now:
                task.is_past_due = True
            elif (task.date_limite - now).days <= 2:
                task.is_near_due = True

    # Liste des responsables pour le filtre (admin)
    responsables = User.objects.all() if request.user.is_superuser else None

    return render(request, 'tasks/task_list.html', {
        'tasks': tasks,
        'responsables': responsables,
    })

@login_required
def task_create(request):
    is_admin = request.user.is_superuser
    if request.method == 'POST':
        form = TaskForm(request.POST, is_admin=is_admin)
        if form.is_valid():
            task = form.save(commit=False)
            # Les utilisateurs normaux ne peuvent créer que pour eux-mêmes
            if not is_admin:
                task.responsable = request.user
            task.save()
            return redirect('task_list')
    else:
        form = TaskForm(is_admin=is_admin)
    return render(request, 'tasks/task_form.html', {'form': form})

@login_required
def task_update(request, pk):
    task = get_object_or_404(Task, pk=pk)
    if task.responsable != request.user and not request.user.is_superuser:
        return redirect('task_list')

    is_admin = request.user.is_superuser
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task, is_admin=is_admin)
        if form.is_valid():
            form.save()
            return redirect('task_list')
    else:
        form = TaskForm(instance=task, is_admin=is_admin)
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