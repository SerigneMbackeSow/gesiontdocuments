from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import csrf_exempt

import facturations
from archivedocuments.models import Utilisateur
from facturations.models import Utilisateurs
from .forms import LoginForm


@csrf_exempt
def login_page(request):
    forms = LoginForm()
    if request.method == 'POST':
        forms = LoginForm(request.POST)
        if forms.is_valid() or 1:
            username = forms.cleaned_data['username']
            password = forms.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                return redirect('dashboard')

    context = {'form': forms}
    return render(request, 'templatetra/login1.html', context)
@csrf_exempt
def acceulli_page(request):
    return render(request, 'templatetra/acceulli.html')
def redirige_app(request,app):
    if app == 'archive' :
       return render(request, 'templatetra/login1.html')
    else :
        return render(request, 'templatetra/login_ged.html')

def signup_page(request):
    forms = facturations.forms.UtilisateurForm()
    return render(request, 'docs/crerutilisateur.html', {'forms': forms})



@csrf_exempt
def seconnecter(request):
    forms = LoginForm()
    if request.method == 'POST':
        if request.POST['app'] == 'archive' :
            forms = LoginForm(request.POST)
            if forms.is_valid()  or 1:
                username = request.POST['email']
                password = request.POST['password']
                user= False
                service='archive'

                try :
                 user= Utilisateur.objects.get(email=username,password=password)
                except:
                    pass
                    forms = LoginForm()
                    context = {'form': forms, 'message': "Login ou Mot de Passe Incorrect!"}
                    return render(request, 'templatetra/login1.html', context)
                return render(request, 'templatetra/index.html', {'util': user, 'service': service})

            forms = LoginForm()
            context = {'form': forms,'message' : "Formulaire Non Valide"}
            return render(request, 'templatetra/login1.html', context)
        else :
            if request.POST['app'] == 'ged' or 1:
                forms = LoginForm(request.POST)
                if forms.is_valid() or 1:
                    username = request.POST['email']
                    password = request.POST['password']
                    user = False
                    service = 'archive'

                    try:
                        user = Utilisateurs.objects.get(email=username, password=password)
                    except:
                        pass
                        forms = LoginForm()
                        context = {'form': forms, 'message': "Login ou Mot de Passe Incorrect!"}
                        return render(request, 'templatetra/login_ged.html', context)
                    return render(request, 'templatetra/index_ged.html', {'util': user, 'service': service})

                forms = LoginForm()
                context = {'form': forms, 'message': "Formulaire Non Valide"}
                return render(request, 'templatetra/login_ged.html', context)
        return render(request, 'templatetra/login_ged.html')




def deconnecter(request,id):
 return redirect('login')





def logout_page(request):
    logout(request)
    return redirect('login')
