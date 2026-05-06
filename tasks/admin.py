from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import Category, Task, ResponsableProfile


# ── Inline pour afficher le profil dans l'admin User ──
class ResponsableProfileInline(admin.StackedInline):
    model = ResponsableProfile
    can_delete = False
    verbose_name_plural = 'Profil Responsable'
    fk_name = 'user'


# ── Personnalisation de l'admin User ──
class CustomUserAdmin(BaseUserAdmin):
    inlines = (ResponsableProfileInline,)
    list_display = ('username', 'first_name', 'last_name', 'email', 'is_staff', 'is_active', 'get_service')
    list_filter = ('is_staff', 'is_active', 'is_superuser')
    search_fields = ('username', 'first_name', 'last_name', 'email')

    def get_service(self, obj):
        try:
            return obj.profile.service
        except ResponsableProfile.DoesNotExist:
            return '—'
    get_service.short_description = 'Service'


# Remplacer l'admin User par défaut
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)


# ── Admin Responsable Profile (aussi accessible directement) ──
@admin.register(ResponsableProfile)
class ResponsableProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'service')
    search_fields = ('user__username', 'user__first_name', 'user__last_name', 'service')
    list_editable = ('service',)


# ── Admin Catégorie ──
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('nom', 'couleur')
    search_fields = ('nom',)
    list_editable = ('couleur',)


# ── Admin Tâche ──
@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('titre', 'responsable', 'statut', 'date_limite', 'categorie')
    list_filter = ('statut', 'responsable', 'categorie', 'date_limite')
    search_fields = ('titre', 'description')
    list_editable = ('statut',)
    list_per_page = 25
    date_hierarchy = 'date_limite'
    ordering = ('-date_limite',)


# ── Personnalisation du site admin ──
admin.site.site_header = 'TaskMaster — Administration'
admin.site.site_title = 'TaskMaster Admin'
admin.site.index_title = 'Gestion des données'