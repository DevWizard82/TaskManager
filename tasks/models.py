from django.db import models
from django.contrib.auth.models import User

class ResponsableProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    service = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.user.username} - {self.service}"

class Category(models.Model):
 
    nom = models.CharField(max_length=100)
    couleur = models.CharField(max_length=20, default='primary')

    def __str__(self):
        return self.nom

class Task(models.Model):

    STATUT_CHOICES = [
        ('A_FAIRE', 'À faire'),
        ('EN_COURS', 'En cours'),
        ('TERMINE', 'Terminé'),
    ]

    titre = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    date_limite = models.DateTimeField(blank=True, null=True)
    statut = models.CharField(max_length=20, choices=STATUT_CHOICES, default='A_FAIRE')
    
    categorie = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    
    responsable = models.ForeignKey(User, on_delete=models.CASCADE, related_name='taches')

    def __str__(self):
        return self.titre