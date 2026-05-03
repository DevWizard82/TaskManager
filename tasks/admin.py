from django.contrib import admin
from .models import Category, Task, ResponsableProfile

@admin.register(ResponsableProfile)
class ResponsableProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'service')
    search_fields = ('user__username', 'service')

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('nom', 'couleur')
    search_fields = ('nom',)

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('titre', 'responsable', 'statut', 'date_limite', 'categorie')
    list_filter = ('statut', 'responsable', 'categorie', 'date_limite')
    search_fields = ('titre', 'description')
    list_editable = ('statut',)