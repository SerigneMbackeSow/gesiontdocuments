import locale
import os
from datetime import datetime
from tkinter.tix import Form

from django.http import HttpResponse
from django.shortcuts import render, redirect

from facturations.forms import UtilisateurForm, UtilisateuwrForm, LoginForm, BoiteForm, ArchiveForm, DocumentForm
from facturations.models import Utilisateurs, DetailsDossier, Boite, Localisation, Document, Permissions, Demande, \
    DemandePermission, Permission


# Create your views here.
def Crer_Utilisateur_page(request):
    if request.method == 'POST':

        forms = UtilisateurForm(request.POST)
        if forms.is_valid() or 1:
            forms.save()
            render(request, 'docs/crerutilisateur.html', {'forms': forms})
        else:
            forms = UtilisateurForm()
        return render(request, 'docs/crerutilisateur.html', {'forms': forms})


def Crer_Utilisateuwr_page(request):
    if request.method == 'POST':
        form = UtilisateuwrForm(request.POST)
        if form.is_valid() or 1:
            cleaned_data = form.cleaned_data
            instance = Utilisateurs(
                nom=form.cleaned_data['nom'],
                prenom=form.cleaned_data['prenom'],
                email=form.cleaned_data['email'],
                password=form.cleaned_data['password'],
                telephone=form.cleaned_data['telephone'],
                # direction=form.cleaned_data['direction'],
                direction=request.POST['direction'],
                role=request.POST['rolee']
                # form.cleaned_data['direction']
            )
            instance.save()
            return redirect('/users/login/')
        else:
            forms = UtilisateurForm()
            return render(request, 'docs/crerutilisateur.html', {'forms': forms})


def login_page(request):
    forms = LoginForm()
    if request.method == 'POST':
        forms = LoginForm(request.POST)
        if forms.is_valid():
            username = forms.cleaned_data['username']
            password = forms.cleaned_data['password']
            try:
                user = Utilisateurs.objects.get(email=username, password=password)
            except:
                return render(request, 'users/login.html')

            if user:
                # request.session['id_user'] = user.id_utilisateur
                return HttpResponse("<strong>You are logged out.{{request.session['id_user']}}</strong>")
                # return render(request, 'docs/dashboard.html', {'util': user})
            # context = {'form': forms}
            # return redirect('/doc/login/')

            return render(request, 'users/login.html')


########################################AGENT#######################################################
def listeboitedirection(request, id):
    lisboite = []
    #a = request.session.get('user_id')
    user = Utilisateurs.objects.get(id_utilisateur=id)
    direction = user.direction
    listuser = Utilisateurs.objects.filter(direction=direction)
    try:
        lisboite = Boite.objects.filter(id_user__in=listuser)
    except:
        pass
    return render(request, 'templatetra/list_boite.html', {'boite': lisboite, 'user': user, 'util': user})

def ajouterboite_page(request, id):
    forms = BoiteForm()
    # id=request.session.get('user_id')
    user = Utilisateurs.objects.get(id_utilisateur=id)
    #return render(request, 'docs/ajouterboite.html', {'form': forms, 'user': user, 'util': user})
    return render(request, 'templatetra/ajout-boite.html', {'form': forms, 'user': user, 'util': user})


def enregistrerboite(request):
    if request.method == 'POST':
        form = BoiteForm(request.POST)
        id_user = request.session.get('user_id')
        if form.is_valid() or 1:
            cleaned_data = form.cleaned_data
            #id_user = cleaned_data['id_user']
            #numero_boite = cleaned_data['numero_boite']
            instance = Boite(
            mention = request.POST['mention'],
            #numero_rang = request.POST['rang'],
            date_creation =datetime.now(),
            id_user =request.POST['id_user']
            #harmoire = request.POST['armoire'],
            #numero_comp = request.POST['compartiment'],
            #niveau = request.POST['niveau'],
            )
            instance.save()
            return  listeboitedirection(request, request.POST['id_user'])

    else:
        return ajouterboite_page(request, request.POST['id_user'])

def listedocumentboite(request, id):
    listedoc = []
    boite=False
    user=False
    try:
        listedoc = Document.objects.filter(id_boite=id)
        boite = Boite.objects.get(id_boite=id)
        user = Utilisateurs.objects.get(id_user=boite.id_user)
    except:
        pass
    return render(request, 'templatetra/list_document.html', {'doc': listedoc, 'user': user, 'util': user, 'boite': boite})

def clotureBoite(request, id):
    boite=False
    user=False
    try:
      boite = Boite.objects.get(id_boite=id)
      boite.etat = 0
      user = Utilisateurs.objects.get(id_user=boite.id_user)
      if boite:
          boite.save()
          return listeboitedirection(request, user.id_utilisateur)
    except:
        pass

    return listedocumentboite(request, id)

####################################################################GESTION DOCUMENT############################################
def ajouterdossier_page(request, id):
    forms = DocumentForm()
    boite = Boite.objects.get(id_boite=id)
    user = Utilisateurs.objects.get(id_utilisateur=boite.id_user)
    #return render(request, 'docs/ajouerterdossier.html', {'form': forms, 'user': user, 'util': user, 'boite': boite})
    return render(request, 'templatetra/ajout-document.html', {'form': forms, 'user': user, 'util': user, 'boite': boite})


def ajouterdocumentboite(request):
    if request.method == 'POST':
        form = BoiteForm(request.POST)
        user=False
        boite=False
        try:
            user=Utilisateurs.objects.get(id_user=request.POST['id_user'])
            boite=Boite.objects.get(id_boite=request.POST['id_boite'])
        except :
           pass
        fichier = form.cleaned_data['document']
        handle_uploaded_file(fichier)
        current_timestamp = int(datetime.timestamp(datetime.now()))
        if form.is_valid() or 1:

            instanceper = Permissions(
                type=2,
                description='tout',
                id_user=request.POST['id_user'],
                # id_documment=derniere_document.id_document
            )
            instanceper.save()
            derniere_per = Permission.objects.latest(' id_permission')
            ####Ajoter Document
            instance=Document( numero_docuemnt =request.POST['numero_docuemnt'],
                                date_creation =datetime.now(),
                                chemin_acces = str(current_timestamp) + fichier.name,
                                eta = request.POST['eta'],
                                client =request.POST['client'] ,
                                nom_navire = request.POST['nom_navire'],
                                numero_voyage =request.POST['numero_voyage'],
                               id_boite =request.POST['id_boite'],
                               id_oer=derniere_per. id_permission,
                               )
            instance.save()

            return  listedocumentboite(request, boite.id_boite)
    else:
        forms = DocumentForm()
        boite = Boite.objects.get(id_boite=request.POST['boite'])
        user = Utilisateurs.objects.get(id_user=boite.id_user)
        return render(request, 'docs/ajouerterdossier.html',
                      {'forms': forms, 'user': user, 'util': user, 'boiie': boite})

def handle_uploaded_file(f):
    current_timestamp = int(datetime.timestamp(datetime.now()))
    with open('static/archives/' + str(current_timestamp) + f.name, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)

def ajouerrestriction(request, id_document):
     instance=Permissions(
                            type='Ok',
                            description = 'ok',
                            id_user='Ok',
                            id_documment=id_document
                            )
     instance.save()
     doc=Document.objects.get(id_document=id_document)
     boite=Boite.objects.get(id_boite=doc.id_boite)
     return listedocumentboite(request, boite.id_boite)

def voir_document(request, id_document):
    fichier_pdf = Document.objects.get(id_document=id_document)
    boite = Boite.objects.get(id_boite=fichier_pdf.id_boite)
    user = Utilisateurs.objects.get(id_user=request.session.get('id_user'))
    return render(request, 'docs/voirfichier.html',
                  {'doc': fichier_pdf, 'user': fichier_pdf.id_user, 'util': user, 'boite': boite})
##################ajouter detail##################################################################
####Gestion demande#######################################
def listedemesddemande(request, id):
    listdmd = []
    a = request.session.get('user_id')
    user = Utilisateurs.objects.get(id_user=id)
    try:
        listdmd = Demande.objects.filter(id_demandeur=id)
    except:
        pass
    return render(request, 'docs/listeboite.html', {'dmd': listdmd, 'user': user, 'util': user})

def ajouterdemande_page(request, id,idobj):
    #forms = DemandeForm()
    # id=request.session.get('user_id')
    user = Utilisateurs.objects.get(id_user=id)
    boite=False
    try:
         boite=Boite.objects.get(id_boite=idobj)
    except:
        pass
    #'form': forms,
    return render(request, 'docs/ajouterboite.html', { 'user': user, 'util': user,'boite':boite})
def ajouterdemande(request):
    if request.method == 'POST':
        form = BoiteForm(request.POST)
        id_user = request.session.get('user_id')
        locale.setlocale(locale.LC_TIME, 'fr_FR.UTF-8')
        now = datetime.now()
        formatted_now = now.strftime("%d %B %Y %H:%M:%S")
        type='document'
        if request.POST['boite']:
            type='boite'
        if form.is_valid() or 1:
            instance=Demande(
                    type=type,
                     commentaire =request.POST['comentaire'] ,
                     date_dmd =datetime.now(),
                    #date_retour =,
                    id_demandeur =request.POST['id_user'] ,
                    #id_accepteur = ,
                    etat =0,
                    id_docuement =request.POST['id_document']  ,
                    id_boite =request.POST['id_boite']  ,

            )
            instance.save()
            return listedemesddemande(request,request.POST['id_user'])

    else:
            return ajouterdemande_page(request, request.POST['id_user'])

def listedemanddeencour(request, id):
    listdmd = []
    a = request.session.get('user_id')
    user = Utilisateurs.objects.get(id_user=id)
    try:
        listdmd = Demande.objects.filter(etat=0)
    except:
        pass
    return render(request, 'docs/listeboite.html', {'dmd': listdmd, 'user': user, 'util': user})

def accepterdemande_page(request,id,id_user):
    # forms = DemandeForm()
    # id=request.session.get('user_id')
    user = Utilisateurs.objects.get(id_user=id_user)
    dmd=Demande.objects.get(id_dmd__gte=id)
    # 'form': forms,
    return render(request, 'docs/ajouterboite.html', {'user': user, 'util': user,'dmd':dmd})
def refuserdemande_page(request,id,id_user):
    # forms = DemandeForm()
    # id=request.session.get('user_id')
    user = Utilisateurs.objects.get(id_user=id_user)
    dmd=Demande.objects.get(id_dmd__gte=id)
    # 'form': forms,
    return render(request, 'docs/ajouterboite.html', {'user': user, 'util': user,'dmd':dmd})

def accepterdeamnde(request):
    if request.method == 'POST':
    #etat passe a 1
              dmd=Demande.objects.get(id_dmd=request.POST['id_dmd'])
              dmd.id_accepteur='ok'
              dmd.commentaire_reponse = request.POST['rescom']
              dmd.eta=1
              dmd.save()
              return listedemanddeencour(request,dmd.id_demandeur)

def refusedemande(request,id,id_user):
    if request.method == 'POST':
            dmd = Demande.objects.get(id_dmd=request.POST['id_dmd'])
            dmd.id_accepteur = id_user
            dmd.id_accepteur =request.POST['id_use']
            dmd.commentaire_reponse = request.POST['rescom']
            dmd.etat=2
            dmd.save()
            return listedemanddeencour(request,dmd.id_demandeur)


###############################################Archiviste######################################################################
def listeboiteAclasser(request, id):
    boite = Boite.objects.filter(etat=0,numero_rang__startswith='Aucune')
    user = Utilisateurs.objects.get(id_user=id)
    return render(request, 'docs/listeboiteclasser.html', {'doc': boite, 'user': user, 'util': user})

def classerBoite_page(request, id, id_user):
    boite = Boite.objects.get(id_boite=id)
    user = Utilisateurs.objects.get(id_user=id_user)
    return render(request, 'docs/ajouterdossierarchiviste.html',
                  { 'user': user, 'util': user, 'boite': boite})
def classerboite(request):
    if request.method == 'POST':
        id = request.POST['id_user']
        id_boite = request.POST['id_boite']
        id_user = request.POST['id_user']
        form = ArchiveForm(request.POST)
        if form.is_valid() or 1:
            boit = Boite.objects.get(id_boite=id_boite)
            boit.numero_rang = request.POST['numerorang']
            boit.armoire = request.POST['armoire']
            boit.numero_comp = request.POST['com']
            boit.niveau = request.POST['niveau']
            boit.etat=1
            boit.save()

            return listeboiteclasser(request, request.POST['id_user'])
        else:

            return classerBoite_page(request, request.POST['id_user'])


def listeboiteclasser(request, id):
    lisboite = []
    user = Utilisateurs.objects.get(id_utilisateur=id)
    try:
        lisboite = Boite.objects.exclude(etat=0, numero_rang__startswith='Auc')
    except:
        pass
    loc = Localisation.objects.all()
    return render(request, 'docs/listeboitearchive.html', {'doc': lisboite, 'user': user, 'util': user, 'loc': loc})

def voir_detail_archive(request, id, id_user):
    boite = Boite.objects.get(id_boite=id)
    user = Utilisateurs.objects.get(id_utilisateur=id_user)
    return render(request, 'docs/detailrang.html', {'detboit': boite, 'user': user, 'util': user})



###########################################################Gestion demnade Permission
def demandepermission_page(request, id, id_user):
    doc = Document.objects.get(id_document=id)
    user = Utilisateurs.objects.get(id_user=id_user)
    return render(request, 'docs/ajouterdossierarchiviste.html',
                  { 'user': user, 'util': user, 'doc': doc})
def enregistrerdemandepermission(request):
    if request.method == 'POST':
        id = request.POST['id_user']
        id_boite = request.POST['id_boite']
        id_user = request.POST['id_user']
        form = ArchiveForm(request.POST)
        if form.is_valid() or 1:
             instance=DemandePermission(
                                         motif_dmd=request.POST['motif'],
                                         #commentaire_vld = request.POST['comentaire'],
                                         date_dmd = datetime.now(),
                                         id_demandeur =id_user ,
                                         #id_valideur = ,
                                         etat = 0 ,
                                         id_per = request.POST['id_per'],
                                         id_document = request.POST['id_document']
                                         )
             instance.save()


def listedemandepermissionencours(request,id):
    user=Utilisateurs.objects.get(id_user=id)
    lstuser=Utilisateurs.objects.filter(direction=user.direction)
    lstboite=Boite.objects.filter(id_user__in=lstuser)
    lstdoc=Document.objects.filter(id_boite__in=lstboite)
    Listdmd=DemandePermission.objects.filter(id_document__in=lstdoc,etat=0)
    return  render(request, 'docs/listeboitearchive.html', {'doc': Listdmd, 'user': user, 'util': user})

def voird_detail_deamnde(request,iddmd,id_user):
    user=Utilisateurs.objects.get(id_user=id)
    dmd=DemandePermission.objects.get(id_dmd_per=iddmd)
    doc=Document.objects.get(id_document=dmd.id_document)
    return  render(request, 'docs/listeboitearchive.html', {'dmd': dmd, 'user': user, 'util': user,'doc':doc})


def accepterdemande_page(request,id,id_user):
    user = Utilisateurs.objects.get(id_user=id_user)
    dmd=DemandePermission.objects.get(id_dmd_per=id)
    return render(request, 'docs/listeboitearchive.html', {'doc': dmd, 'user': user, 'util': user})

def repondredemandepermission(request):
        if request.method == 'POST':
            id_user=Utilisateurs.objects.get(request.POST['id_user'])
            type=request.POST['type']
            dmd=DemandePermission.objects.get(id_dmd_per=request.POST['id_dmd_per'])
            dmd.id_valideur=request.POST['id_user'],
            dmd.commentaire_vld=request.POST['comentaire_vld']
            dmd.etat=1
            if type=='refuser':
                dmd.eta=2
            dmd.save()
            return  listedemandepermissionencours(request,id_user)







"""


#####ARCHIVE
def Listearchive(request, id):
    listedoc = []
    a = request.session.get('user_id')
    try:
        listedoc = Dossier.objects.filter(id_boite=id)
        # listedoc = Dossier.objects.filter(id_user=a)
        # user=Utilisateurs.objects.get(id_user=id)
    except:
        pass
    boite = Boite.objects.get(id_boite=id)
    id_user = boite.id_user
    user = Utilisateurs.objects.get(id_utilisateur=id)
    # user = Utilisateurs.objects.get(id_utilisateur=a)
    return render(request, 'docs/archivefact.html', {'doc': listedoc, 'user': user, 'util': user, 'boite': boite})


def ajouterdossier_page(request, id):
    forms = DossierForm()
    boite = Boite.objects.get(id_boite=id)
    user = Utilisateurs.objects.get(id_utilisateur=boite.id_user)
    return render(request, 'docs/ajouerterdossier.html', {'form': forms, 'user': user, 'util': user, 'boite': boite})


def telecharger_fichier(request):
    listedoc = []
    if request.method == 'POST':
        form = DossierForm(request.POST, request.FILES)
        if form.is_valid() or 1:
            fichier = form.cleaned_data['document']
            # id_user=form.cleaned_data['user']
            user = Utilisateurs.objects.get(id_utilisateur=request.POST['user'])
            # handle_uploaded_file(fichier.name)
            handle_uploaded_file(fichier)
            # Définir la locale française
            locale.setlocale(locale.LC_TIME, 'fr_FR.UTF-8')

            # Obtenez la date et l'heure actuelles
            now = datetime.now()

            # Formatez la date et l'heure avec les noms des mois en français
            formatted_now = now.strftime("%d %B %Y %H:%M:%S")
            current_timestamp = int(datetime.timestamp(datetime.now()))

            instance = Dossier(chemin_acces=str(current_timestamp) + fichier.name,
                               numero_dossier=form.cleaned_data['numero_dossier'],
                               id_boite=request.POST['boite'],
                               id_user=request.POST['user'],
                               date_creation=datetime.now()
                               # date_creation = formatted_now
                               )  # Enregistrez le nom du fichier comme chemin d'accès, vous pouvez changer cette logique
            instance.save()

            listedoc = []
            try:
                listedoc = Dossier.objects.filter(id_boite=request.POST['boite'])
                # user=Utilisateurs.objects.get(id_u=id)
            except:
                pass
        boite = Boite.objects.get(id_boite=request.POST['boite'])
        user = Utilisateurs.objects.get(id_utilisateur=boite.id_user)
        return render(request, 'docs/archivefact.html', {'doc': listedoc, 'user': user, 'util': user, 'boite': boite})

    else:
        forms = DossierForm()
        boite = Boite.objects.get(id_boite=request.POST['boite'])
        user = Utilisateurs.objects.get(id_utilisateur=boite.id_user)
        # user = Utilisateurs.objects.get(id_user=id)
        return render(request, 'docs/ajouerterdossier.html',
                      {'forms': forms, 'user': user, 'util': user, 'boiie': boite})





def voir_pdf(request, pdf_id):
    fichier_pdf = Dossier.objects.get(numero_dossier=pdf_id)
    boite = Boite.objects.get(id_boite=fichier_pdf.id_boite)
    fichier = 'certificat_inscription_master1_SIR.pdf'
    user = Utilisateurs.objects.get(id_utilisateur=request.session.get('id_user'))
    return render(request, 'docs/voirfichier.html',
                  {'doc': fichier_pdf, 'user': fichier_pdf.id_user, 'util': user, 'boite': boite})


###DeatilleDossier
def voir_detail(request, id):
    forms = DetailDossierForm()
    loc = []
    try:
        dossier = Dossier.objects.get(numero_dossier=id)
        det = DetailsDossier.objects.get(id_dossier=id)
        loc = Localisation.objects.filter(numero_dossier=id)
        forms = DetailDossierForm(initial={
            'eta': det.eta,
            'nom_navire': det.nom_navire,
            'numero_voyage': det.numero_voyage,
            'localisation': det.localisation,
            'numer_boite': det.numer_boite,
            'carton': det.carton,
            'classeur': det.classeur,

        })
    except:
        pass
    user = Utilisateurs.objects.get(id_utilisateur=request.session.get('id_user'))
    dossier = Dossier.objects.get(numero_dossier=id)
    boite = Boite.objects.get(id_boite=dossier.id_boite)
    # return listeaaarchboite(request,boite.id_boite)

    return render(request, 'docs/detaildossier.html',
                  {'forms': forms, 'dossier': dossier, 'util': user, 'boite': boite, 'loc': loc})


def ajouterdetail(request):
    if request.method == 'POST':
        form = DetailDossierForm(request.POST)
        if form.is_valid() or 1:
            id_doosier = request.POST['dossier']
            # numerpbl=request.POST['numerobl']
            cleaned_data = form.cleaned_data
            instance = DetailsDossier(
                id_dossier=id_doosier,
                numero_bl='BK2345',
                eta=form.cleaned_data['eta'],
                nom_navire=form.cleaned_data['nom_navire'],
                numero_voyage=form.cleaned_data['numero_voyage'],
                localisation='local',
                # numer_boite =form.cleaned_data['numer_boite'] ,
                numer_boite=request.POST['numero_boite'],
                carton='cart',
                classeur=form.cleaned_data['classeur'],

            )
            instance.save()
        id = request.POST['id_boite']
        return listeaaarchboite(request, id)


    else:

        forms = DetailDossierForm()
        dossier = Dossier.objects.get(numero_dossier=id)
        user = Utilisateurs.objects.get(id_utilisateur=request.session.get('id_user'))
        return render(request, 'docs/detaildossier.html', {'forms': forms, 'dossier': dossier, 'util': user})


def recherchebl(request):
    if request.method == 'POST':
        id_user = request.POST['id_user']
        id = request.POST['id_boite']
        bl = request.POST['bl']
        listedoc = []
        # rresponse = f""

        # return HttpResponse('<p>id_user: </p>'+{{id_user}})
        # listedoc = Dossier.objects.filter(id_boite=request.POST['id_boite'])

        try:
            listedoc = Dossier.objects.filter(numero_dossier=bl)
        # user=Utilisateurs.objects.get(id_user=id)
        except:
            pass
        if listedoc:

            boite = Boite.objects.get(id_boite=id)
            user = Utilisateurs.objects.get(id_utilisateur=boite.id_user)
            # useru = Utilisateurs.objects.get(id_utilisateur=request.session.get('id_user'))
            return render(request, 'docs/archivefact.html',
                          {'doc': listedoc, 'user': user, 'util': user, 'boite': boite})
        else:

            # id=request.POST['id_boite'])
            return listeaaarchboite(request, id)

    # return render(request, 'docs/archivefact.html')









def listeaaarchboite(request, id):
    listedoc = []
    boite = Boite.objects.get(id_boite=id)
    try:
        listedoc = Dossier.objects.filter(id_boite=id)
        # listedoc = Dossier.objects.filter(id_user=a)
        # user=Utilisateurs.objects.get(id_user=id)
    except:
        pass
    user = Utilisateurs.objects.get(id_utilisateur=boite.id_user)
    # user = Utilisateurs.objects.get(id_utilisateur=a)
    return render(request, 'docs/archivefact.html', {'doc': listedoc, 'user': user, 'util': user, 'boite': boite})


##ARCHIVE
def login_page_archiviste(request):
    forms = UtilisateurForm()
    return render(request, 'docs/login_archiviste.html', {'forms': forms})


#####
def listeHarmoire(request, id):
    listedoc = []
    # boite = Localisation.objects.get(id_user=id)
    try:
        listedoc = Localisation.objects.filter(id_user=id)
        # listedoc = Dossier.objects.filter(id_user=a)
        # user=Utilisateurs.objects.get(id_user=id)
    except:
        pass
    user = Utilisateurs.objects.get(id_utilisateur=id)
    # user = Utilisateurs.objects.get(id_utilisateur=a)
    return render(request, 'docs/listedossierarchivite.html', {'doc': listedoc, 'user': user, 'util': user})


def classerdossierarchivist_page(request, id, id_user):
    forms = ArchiveForm()
    boite = Boite.objects.get(id_boite=id)
    user = Utilisateurs.objects.get(id_utilisateur=id_user)
    return render(request, 'docs/ajouterdossierarchiviste.html',
                  {'form': forms, 'user': user, 'util': user, 'boite': boite})


def entregistrerdossierarchives(request):
    if request.method == 'POST':
        id = request.POST['id_user']
        id_boite = request.POST['id_boite']
        id_user = request.POST['id_user']
        form = ArchiveForm(request.POST)
        if form.is_valid() or 1:
            cleaned_data = form.cleaned_data

            boit = Boite.objects.get(id_boite=id_boite)
            boit.numero_rang = request.POST['numerorang']
            boit.harmoire = request.POST['armoire']
            boit.numero_comp = request.POST['com']
            boit.niveau = request.POST['niveau']
            boit.save()
            instance = Localisation(
                id_harmoire=request.POST['armoire'],
                niveau=request.POST['niveau'],

                numero_comp=request.POST['com'],

                numero_dossier=boit.id_boite,
                id_user=request.POST['id_user']

            )
            instance.save()

            return listeboiteclasser(request, request.POST['id_user'])
        else:

            return classerdossierarchivist_page(request, request.POST['id_user'])


def toutdossier(request, id):
    listedoc = []
    try:
        user = Utilisateurs.objects.get(id_utilisateur=id)
        direction = user.direction
        listeuser = Utilisateurs.objects.filter(direction=direction)
        listedoc = Dossier.objects.filter(id_user__in=listeuser)
    except:
        pass
    user = Utilisateurs.objects.get(id_utilisateur=id)
    return render(request, 'docs/toutdossier.html', {'doc': listedoc, 'user': user, 'util': user})


def update(request, id):
    boite = Boite.objects.get(id_boite=id)
    user = Utilisateurs.objects.get(id_utilisateur=boite.id_user)
    boite.etat = True
    if boite:
        boite.save()
        return listeboite(request, user.id_utilisateur)

    return listeaaarchboite(request, id)


def liste_doosier_boite(request, id):
    boite = Boite.objects.get(numero_boite=id)
    dossier = Dossier.objects.filter(id_boite=id)
    return


def listeboitearchive(request, id):
    lisboite = []
    # a = request.session.get('user_id')
    user = Utilisateurs.objects.get(id_utilisateur=id)
    # direction=user.direction
    # listuser=Utilisateurs.objects.filter(direction=direction)
    try:
        lisboite = Boite.objects.filter(etat=True, numero_rang__startswith='Auc')
    except:
        pass
    loc = Localisation.objects.all()
    return render(request, 'docs/listeboitearchive.html', {'doc': lisboite, 'user': user, 'util': user, 'loc': loc})


def listeboiteclasser(request, id):
    boite = Boite.objects.exclude(numero_rang__startswith='Aucune')
    loc = Localisation.objects.all()
    user = Utilisateurs.objects.get(id_utilisateur=id)
    return render(request, 'docs/listeboiteclasser.html', {'doc': boite, 'user': user, 'util': user, 'loc': loc})


def detailrang(request, id, id_user):
    boite = Boite.objects.get(id_boite=id)
    dossier = Dossier.objects.filter(id_boite=id)

    user = Utilisateurs.objects.get(id_utilisateur=id_user)

    loc = Localisation.objects.get(numero_dossier=id)
    # user = Utilisateurs.objects.get(id_utilisateur=loc.id_user)
    return render(request, 'docs/detailrang.html',
                  {'detboit': boite, 'user': user, 'util': user, 'loc': loc, 'dos': dossier})


def voir_pdf_archive(request, pdf_id, id_user):
    fichier_pdf = Dossier.objects.get(numero_dossier=pdf_id)
    boite = Boite.objects.get(id_boite=fichier_pdf.id_boite)
    # fichier = 'certificat_inscription_master1_SIR.pdf'
    user = Utilisateurs.objects.get(id_utilisateur=id_user)
    return render(request, 'docs/voirfichierarchive.html',
                  {'doc': fichier_pdf, 'user': user, 'boite': boite, 'util': user})


def annulerarchive(request, id, id_user):
    return detailrang(request, id, id_user)


def detaildossierarchive(request, id, id_user):
    dossier = Dossier.objects.get(numero_dossier=id)
    detdo = False
    try:
        detdo = DetailsDossier.objects.get(id_dossier=id)
    except:
        detdo = True
        pass
    boite = Boite.objects.get(id_boite=dossier.id_boite)
    # fichier = 'certificat_inscription_master1_SIR.pdf'
    user = Utilisateurs.objects.get(id_utilisateur=id_user)
    loc = Localisation.objects.get(numero_dossier=boite.id_boite)
    return render(request, 'docs/detaildossierarchive.html',
                  {'dossier': dossier, 'util': user, 'detdo': detdo, 'boite': boite, 'loc': loc, 'detdo': detdo})
    # return  detailrang(request,id,id_user)


def voir_pdf_tout(request, pdf_id):
    fichier_pdf = Dossier.objects.get(numero_dossier=pdf_id)
    boite = Boite.objects.get(id_boite=fichier_pdf.id_boite)
    fichier = 'certificat_inscription_master1_SIR.pdf'
    user = Utilisateurs.objects.get(id_utilisateur=request.session.get('id_user'))
    return render(request, 'docs/voirfichiertout.html',
                  {'doc': fichier_pdf, 'user': fichier_pdf.id_user, 'util': user, 'boite': boite})


def voir_detailtout(request, id):
    forms = DetailDossierForm()
    loc = []
    try:
        dossier = Dossier.objects.get(numero_dossier=id)
        det = DetailsDossier.objects.get(id_dossier=id)
        loc = Localisation.objects.filter(numero_dossier=id)
        forms = DetailDossierForm(initial={
            'eta': det.eta,
            'nom_navire': det.nom_navire,
            'numero_voyage': det.numero_voyage,
            'localisation': det.localisation,
            'numer_boite': det.numer_boite,
            'carton': det.carton,
            'classeur': det.classeur,

        })
    except:
        pass
    user = Utilisateurs.objects.get(id_utilisateur=request.session.get('id_user'))
    dossier = Dossier.objects.get(numero_dossier=id)
    boite = Boite.objects.get(id_boite=dossier.id_boite)
    # return listeaaarchboite(request,boite.id_boite)

    #return render(request, 'docs/detailstout.html', {'forms': forms, 'dossier': dossier, 'util': user, 'boite': boite, 'loc': loc})
"""