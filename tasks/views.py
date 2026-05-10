from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponseForbidden
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone
from datetime import timedelta
from .models import Task
from .forms import TaskForm
from django.contrib.auth import login
from .models import ResponsableProfile
from .forms import CustomUserCreationForm

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

    now = timezone.now()
    if date_filtre == 'depassee':
        tasks = tasks.filter(date_limite__lt=now)
    elif date_filtre == 'aujourd_hui':
        tasks = tasks.filter(date_limite__date=now.date())
    elif date_filtre == 'semaine':
        tasks = tasks.filter(date_limite__lte=now + timedelta(days=7), date_limite__gte=now)
    elif date_filtre == 'mois':
        tasks = tasks.filter(date_limite__lte=now + timedelta(days=30), date_limite__gte=now)

    if request.user.is_superuser and responsable_id:
        tasks = tasks.filter(responsable_id=responsable_id)

    tasks = tasks.order_by('date_limite')

    for task in tasks:
        task.is_past_due = task.is_overdue()
        task.is_near_due = False
        if task.date_limite and not task.is_past_due and task.statut != 'TERMINE':
            if (task.date_limite - now).days <= 2:
                task.is_near_due = True

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

    ancien_responsable = task.responsable
    is_admin = request.user.is_superuser
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task, is_admin=is_admin)
        if form.is_valid():
            task = form.save()
            if is_admin and task.responsable != ancien_responsable and task.responsable.email:
                try:
                    send_mail(
                        subject='Tâche assignée — TaskMaster',
                        message=f'Bonjour {task.responsable.username},\n\n'
                                f'La tâche "{task.titre}" vous a été assignée.\n'
                                f'Date limite : {task.date_limite or "Non définie"}\n\n'
                                f'— TaskMaster',
                        from_email=settings.DEFAULT_FROM_EMAIL if hasattr(settings, 'DEFAULT_FROM_EMAIL') else 'noreply@taskmaster.local',
                        recipient_list=[task.responsable.email],
                        fail_silently=True,
                    )
                except Exception:
                    pass 
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


@login_required
def task_change_statut(request, pk):
    """Endpoint dédié au changement de statut d'une tâche (POST uniquement)."""
    task = get_object_or_404(Task, pk=pk)

    if task.responsable != request.user and not request.user.is_superuser:
        return HttpResponseForbidden("Non autorisé")

    if request.method == 'POST':
        nouveau_statut = request.POST.get('statut')
        task.change_statut(nouveau_statut)

    return redirect('task_list')


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