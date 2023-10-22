from authentication.models import User, UserManager
from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .forms import UserAdminCreationForm, UserAdminChangeForm

User = get_user_model()

# Supprimer le modèle de groupe de l'administrateur. Nous ne l'utilisons pas.
admin.site.unregister(Group)

class UserAdmin(BaseUserAdmin):
# Les formulaires pour ajouter et modifier des instances d'utilisateur
    form = UserAdminChangeForm
    add_form = UserAdminCreationForm

    # Les champs à utiliser pour afficher le modèle User.
    # Celles-ci remplacent les définitions de la baseUserAdmin
    # qui font référence à des champs spécifiques sur auth.User.
    list_display = ['email', 'admin','staff', 'first_name', 'last_name', 'admin']
    list_filter = ['admin', 'first_name', 'last_name']
    
    fieldsets = (
    ('Information de connexion', {'fields': ('email', 'password',)}),
    ('Personal info', {'fields': ('phone','first_name', 'last_name',)}),
    ('Permissions', {'fields': ('admin', 'is_active', 'staff', )}),
    )
   
    # add_fieldsets n'est pas un attribut ModelAdmin standard. UtilisateurAdmin
    # remplace get_fieldsets pour utiliser cet attribut lors de la création d'un utilisateur.
    add_fieldsets = (
    (None, {
    'classes': ('wide',),
    'fields': ('email', 'password', 'password_2')}
    ),
    )
    search_fields = ['email']
    ordering = ['email']
    filter_horizontal = ()


admin.site.register(User, UserAdmin)








