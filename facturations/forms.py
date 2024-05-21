from django import forms

from .models import Utilisateurs, Localisation, Document, Demande
from .models import Boite

class UtilisateurForm(forms.ModelForm):
    class Meta:
        model = Utilisateurs
        fields = '__all__'

class UtilisateuwrForm(forms.Form):

    nom= forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Votre Nom',
        'type' : "text",
        'id': 'nom',
        'data-val': 'true',
        'data-val-required': 'Please enter name',
    }))
    prenom = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Votre Prenom',
        'type': "text",
        'id': 'prenom',
        'data-val': 'true',
        'data-val-required': 'Please enter name',
    }))
    email = forms.CharField(widget=forms.EmailInput(attrs={
        'class': 'form-control',
        'id': 'email',
        'data-val': 'true',
        'placeholder': 'Votre Email',

        'type': 'email',
        'data-val-required': 'Please enter email',
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'id': 'password',

        'type':'password',
        'placeholder': 'Votre mot de passe',

        'data-val': 'true',
        'data-val-required': 'Please enter password',
    }))
    telephone = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'id': 'telephone',
        'placeholder': 'Votre numéro telephone',
        'type': "number",
        'data-val': 'true',
        'data-val-required': 'Please enter name',
    }))
    direction =forms.ChoiceField(choices=(('FACTURATION', 'FACTURATION'),
                                           ('COMPTABILITE', 'COMPTABILITE'),
                                           ('DOCUMENTATION', 'DOCUMENTATION'),
                                          ('ARCHIVE', 'ARCHIVE'),
                                                  ),
                                  widget=forms.Select(attrs={
                                      'class': 'form-control',

                                      'type': "number",


                                      'id': 'direction',
                                      'data-val': 'true',
                                      'data-val-required': 'Please select a direction',
                                  }))
    role = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'id': 'role',
        'placeholder': 'Votre numéro telephone',
        'type': "text",
        'data-val': 'true',
        'data-val-required': 'Please enter name',
    }))
    class Meta:
        model = Utilisateurs
        fields = '__all__'

class BoiteForm(forms.Form):
        mention = forms.CharField(widget=forms.TextInput(attrs={
            'class': 'form-control',
            'id': 'bt',
            'placeholder': 'Mention Boite',
            'type': "text",
            'data-val': 'true',
            'data-val-required': 'Please enter la mention de la boite',
        }))
        numero_rangement = forms.CharField(widget=forms.TextInput(attrs={
            'class': 'form-control',
            'id': 'numerorang',
            'placeholder': 'Numero Rangement',
            'type': "text",
            'data-val': 'true',
            'data-val-required': 'Please enter la mention de la boite',
        }))

        armoire = forms.CharField(widget=forms.TextInput(attrs={
            'class': 'form-control',
            'id': 'harmoire',
            'placeholder': 'Numeroi Armoire',
            'type': "text",
            'data-val': 'true',
            'data-val-required': 'Please enter name',
        }))
        niveau = forms.CharField(widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Niveau',
        }))
        compartiment = forms.CharField(widget=forms.TextInput(attrs={
            'class': 'form-control',
            'id': 'com',
            'placeholder': 'Numeroi Compartiemnt',
            'type': "text",
            'data-val': 'true',
            'data-val-required': 'Please enter name',
        }))

        class Meta:
            model = Boite




class DocumentForm(forms.Form):
    numero_document=forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'id': 'bth',
        'placeholder': 'Le numero du document',
        'type': "text",
        'data-val': 'true',
        'data-val-required': 'Please enter',
    }))

    eta = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': ' E T A',

        'type': "text",
        'data-val': 'true',
        'data-val-required': 'Please enter',
    }))
    nom_navire = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': ' nom Navire',
        'type': "text",
        'data-val': 'true',
        'data-val-required': 'Please enter',
    }))
    numero_voyage = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Numero Voyage',
        'type': "text",
        'data-val': 'true',
        'data-val-required': 'Please enter',
    }))
    numero_conteneur = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Le numero du conteneur',
        'type': "text",
        'data-val': 'true',
        'data-val-required': 'Please enter',
    }))
    client = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Mention Boite',
        'type': "text",
        'data-val': 'true',
        'data-val-required': 'Please enter',

    }))
    carton = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Carton',
    }))
    classeur = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Classeur',
    }))

    class Meta:
        model = Document
        fields = '__all__'





class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Username',
    }))
    password = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Password',
        'type': 'password'
    }))

class DeamndeForm(forms.Form):
    type= forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'id': 'com',
        'placeholder': 'Numeroi Compartiemnt',
        'type': "text",
        'data-val': 'true',
        'data-val-required': 'Please enter name',
    }))
    class Meta:
        model = Demande



class ArchiveForm(forms.ModelForm):
    id_harmoire = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Numero Harmoire',
    }))
    niveau= forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Niveau',
    }))
    numero_comp = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Numero Compartimenet',
    }))

    numero_dossier = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Numero Rangement',
    }))

    class Meta:
        model = Localisation
        fields = '__all__'