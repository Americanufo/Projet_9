from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model  # Importer get_user_model

User = get_user_model()  # Récupérer le modèle utilisateur 

class SignupForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User  
        fields = ('username', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'placeholder': "Nom d'utilisateur"})
        self.fields['password1'].widget.attrs.update({'placeholder': "Mot de passe"})
        self.fields['password2'].widget.attrs.update({'placeholder': "Confirmer mot de passe"})
