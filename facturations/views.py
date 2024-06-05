import locale
import os
from datetime import datetime
from tkinter.tix import Form

from django.http import HttpResponse
from django.shortcuts import render, redirect

from facturations.forms import UtilisateurForm, UtilisateuwrForm, LoginForm, BoiteForm, ArchiveForm, DocumentForm
from facturations.models import Utilisateurs, DetailsDossier, Boite, Localisation, Document, Permissions, Demande, \
    DemandePermission, Permission, RestrictionDocument


# Create your views here.
def Crer_Utilisateur_page(request):
        forms = UtilisateurForm(request.POST)
        return render(request, 'templatetra/ajout-utilisateur.html', {'forms': forms})



def enregistrer_Utilisateur(request):
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
                #role=request.POST['rolee']
                role='agent'
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
    lst_dt_dmd=Demande.objects.filter(id_demandeur=id)
    restricted_doc_ids = set(lst_dt_dmd.values_list('id_boite', flat=True))
    try:
        lisboite = Boite.objects.filter(id_user__in=listuser)
        for bt in lisboite:
            if bt.id_boite in restricted_doc_ids:
                bt.cons=1
            else :
                 bt.cons=0
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
        if Boite.objects.filter(mention=request.POST['mention']).exists():
            return ajouterboite_page(request, request.POST['id_user'])
            #cleaned_data = form.cleaned_data
        else :
            instance = Boite(
            mention = request.POST['mention'],
            date_creation =datetime.now(),
            id_user =request.POST['id_user']
            )
            instance.save()
            return  listeboitedirection(request, request.POST['id_user'])

    else:
        return ajouterboite_page(request, request.POST['id_user'])

def listedocumentboite(request, id,id_user):
    listedoc = []
    boite=False
    listres=RestrictionDocument.objects.filter(id_user=id_user)
    #listres_dmd= RestrictionDocument.objects.filter(id_user=id_user,etat=0)
    listresdmd = RestrictionDocument.objects.filter(id_user=id_user,etat=0)
    listresdmd_refut = RestrictionDocument.objects.filter(id_user=id_user, etat=3)
    user=False

    try:
        listedoc = Document.objects.filter(id_boite=id)

        boite = Boite.objects.get(id_boite=id)

    except:
        pass
    restricted_doc_ids = set(listres.values_list('id_doc', flat=True))
    restricted_doc_ids_dmd = set(listresdmd.values_list('id_doc', flat=True))
    restricted_doc_ids_dmd_refut = set(listresdmd_refut.values_list('id_doc', flat=True))
    lst_doc_dmd = Demande.objects.filter(id_demandeur=id_user)
    restricted_doc_dmd_ids = set(lst_doc_dmd.values_list('id_docuement', flat=True))

    # Ajouter dynamiquement l'attribut 'acces=0' aux documents restreints dans listedoc
    for doc in listedoc:
        if doc.id_document in restricted_doc_dmd_ids:
             doc.cons = 0
        else :
            doc.cons = 1
        if doc.id_document in restricted_doc_ids_dmd_refut:
            doc.ref=1
        else :
            doc.ref=0

        if doc.id_document in restricted_doc_ids:
            doc.acces = 0
            doc.etat=1
            doc.dmd=0
            if doc.id_document in restricted_doc_ids_dmd:
                doc.acces = 0
                doc.etat = 0
                doc.dmd=1



        else:
            doc.acces = 1  # Ou une autre valeur par défaut si nécessaire
            doc.etat = 3

            doc.dmd = 0

    # Utiliser 'listedoc' dans le contexte ou faire ce que vous devez faire
    context = {
        'listedoc': listedoc,
    }
    user = Utilisateurs.objects.get(id_utilisateur=id_user)
    return render(request, 'templatetra/list_document_agent.html', {'doc': listedoc, 'user': user, 'util': user, 'boite': boite})

def clotureBoite(request, id):
    boite=False
    user=False
    try:
      boite = Boite.objects.get(id_boite=id)
      boite.etat = 0
      boite.save()

    except:
        pass
    user = Utilisateurs.objects.get(id_utilisateur=boite.id_user)
    if boite:

        return listeboitedirection(request, user.id_utilisateur)

    return listedocumentboite(request, id)
def voir_detail_boite(request, id,id_user):
    boite=False
    user=False
    try:
      boite = Boite.objects.get(id_boite=id)

    except:
        pass
    user = Utilisateurs.objects.get(id_utilisateur=id_user)
    if boite:
        return render(request, 'templatetra/detail_boite.html',
                      {'boite': boite, 'user': user, 'util': user})
    else:
        return listeboitedirection(request, user.id_utilisateur)

def updateboite(request):
    boite = False
    user = False
    try:
        boite = Boite.objects.get(id_boite=request.POST['id_boite'])

    except:
        pass
    user = Utilisateurs.objects.get(id_utilisateur=request.POST['id_user'])
    if boite:
        boite.mention=request.POST['mention']
        boite.save()
        return listeboitedirection(request, user.id_utilisateur)
    else:
        return voir_detail_boite(request, boite.id_boite)


def voire_document(request, id,id_user):
    doc=Document.objects.get(id_document=id)
    user=Utilisateurs.objects.get(id_utilisateur=id_user)
    return render(request, 'templatetra/voir_document.html',
                  { 'doc': doc,'util':user})



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
        fichier = request.FILES['file']
        handle_uploaded_file(fichier)
        current_timestamp = int(datetime.timestamp(datetime.now()))
        if form.is_valid() or 1:

            instanceper = Permissions(
                type=2,
                description='tout',
                id_user=request.POST['id_user'],
                # id_documment=derniere_document.id_document
            )
            #instanceper.save()
            #derniere_per = Permission.objects.latest(' id_permission')
            ####Ajoter Document
            if Document.objects.filter(numero_docuemnt=request.POST['numero']).exists():
                return ajouterdossier_page(request, request.POST['id_boite'])
            instance=Document( numero_docuemnt =request.POST['numero'],
                                date_creation =datetime.now(),
                                chemin_acces = str(current_timestamp) + fichier.name,
                                eta = request.POST['eta'],
                               bl= request.POST['bl'],
                                client =request.POST['client'] ,
                                nom_navire = request.POST['navire'],
                                numero_voyage =request.POST['voyage'],
                               id_boite =request.POST['id_boite'],
                               id_per=2
                               )
            instance.save()

            return  listedocumentboite(request,request.POST['id_boite'],request.POST['id_user'])
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
def listedemesddemandeConsultation(request, id):
    listdmd = []
    a = request.session.get('user_id')
    user = Utilisateurs.objects.get(id_utilisateur=id)
    try:
        #listdmd = Demande.objects.filter(id_demandeur=id)
        listdmd = Demande.objects.filter(etat=0)
    except:
        pass
    lst_doc=Document.objects.all()
    #lst_user=Utilisateurs.objects.all()
    lst_boite = Boite.objects.all()
    restricted_boite_ids = set(lst_boite.values_list('id_boite', flat=True))
    restricted_doc_ids = set(lst_doc.values_list('id_document', flat=True))
    #restricted_user_ids = set(lst_boite.values_list('id_utilisateur', flat=True))
    for doc in listdmd:
        if doc.type == "document":
            doc.bt = 0
            if doc.id_docuement in restricted_doc_ids:
                docu=Document.objects.get(id_document=doc.id_docuement)
                doc.numero=docu.numero_docuemnt

                user=Utilisateurs.objects.get(id_utilisateur=doc.id_demandeur)
                doc.user= user.nom + ' '+user.prenom
        else :
            doc.bt = 1
            if doc.id_boite in restricted_boite_ids:
                boite = Boite.objects.get(id_boite=doc.id_boite)
                doc.numero = boite.mention
                doc.id_docuement = ''
                doc.id_boite = boite.id_boite
                user = Utilisateurs.objects.get(id_utilisateur=doc.id_demandeur)
                doc.user = user.nom  + ' '+ user.prenom

    return render(request, 'templatetra/list_demande.html', {'dmd': listdmd, 'user': user, 'util': user})

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
    user = Utilisateurs.objects.get(id_utilisateur=id)
    #return render(request, 'docs/listeboiteclasser.html', {'doc': boite, 'user': user, 'util': user})

    return render(request, 'templatetra/liste_boite_cloture.html', {'boite': boite, 'user': user, 'util': user})
def classerBoite_page(request, id, id_user):
    boite = Boite.objects.get(id_boite=id)
    user = Utilisateurs.objects.get(id_utilisateur=id_user)
    return render(request, 'templatetra/classer_boite.html',
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
            boit.harmoire = request.POST['armoire']
            boit.numero_comp = request.POST['com']
            boit.niveau = request.POST['niveau']
            #boit.etat=1
            boit.save()

            return listeboiteclasser(request, request.POST['id_user'])
        else:

            return classerBoite_page(request, request.POST['id_user'])


def listeboiteclasser(request, id):
    lisboite = []
    user = Utilisateurs.objects.get(id_utilisateur=id)
    try:
        lisboite = Boite.objects.exclude(numero_rang__startswith='Auc')
    except:
        pass
    loc = Localisation.objects.all()
    return render(request, 'templatetra/liste_boite_classer.html', {'boite': lisboite, 'user': user, 'util': user, 'loc': loc})

def voir_detail_archive(request, id, id_user):
    boite = Boite.objects.get(id_boite=id)
    user = Utilisateurs.objects.get(id_utilisateur=id_user)
    return render(request, 'templatetra/detail_archiviste.html', {'boite': boite, 'user': user, 'util': user})

def updateboite_archiviste(request):
    boit = False
    user = False
    try:
        boit = Boite.objects.get(id_boite=request.POST['id_boite'])

    except:
        pass
    user = Utilisateurs.objects.get(id_utilisateur=request.POST['id_user'])
    if boit:
        if request.POST['numero_rang']:
            boit.numero_rang = request.POST['numero_rang']
        boit.harmoire = request.POST['armoire']
        if request.POST['armoire']:
            boit.harmoire = request.POST['armoire']

        if request.POST['com']:
            boit.numero_comp = request.POST['com']
        if request.POST['niveau']:
            boit.niveau = request.POST['niveau']
        boit.save()
        return listeboiteclasser(request, user.id_utilisateur)

    else:
        return voir_detail_archive(request, boit.id_boite,user.id_utilisateur)


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



###########################GESTION EQUIPE
def list_agent(request,id):
    listagent = []
    #a = request.session.get('user_id')
    user = Utilisateurs.objects.get(id_utilisateur=id)
    try:
        listagent = Utilisateurs.objects.filter(role='agent',direction=user.direction)
    except:
        pass
    return render(request, 'templatetra/list_agent.html', {'agt': listagent, 'user': user, 'util': user})

def Crer_agent_page(request,id):
        forms = UtilisateurForm(request.POST)
        user=Utilisateurs.objects.get(id_utilisateur=id)
        return render(request, 'templatetra/crer_agent.html', {'forms': forms,'util':user})

def enregistrer_agent(request):
    if request.method == 'POST':
        form = UtilisateuwrForm(request.POST)
        user=Utilisateurs.objects.get(id_utilisateur=request.POST["id_user"])
        if form.is_valid() or 1:
            cleaned_data = form.cleaned_data
            instance = Utilisateurs(
                nom=request.POST['nom'],
                prenom=request.POST['prenom'],
                email=request.POST['email'],
                password='passer',
                telephone=request.POST['telephone'],
                # direction=request.POST['direction'],
                direction=user.direction,
                #role=request.POST['rolee']
                role='agent'
                # form.cleaned_data['direction']
            )
            instance.save()
            #return redirect('/users/login/')
            return list_agent(request,user.id_utilisateur)
        else:
            forms = UtilisateurForm()
            return Crer_agent_page(request, request.POST["id_user"])
            #return render(request, 'templatetra/crer_agent.html', {'forms': forms})

def update_agent_page(request,id_user,id_agt):
    user=Utilisateurs.objects.get(id_utilisateur=id_user)
    agt=Utilisateurs.objects.get(id_utilisateur=id_agt)
    return render(request, 'templatetra/update_agent.html', {'agt':agt,'util':user,'user':agt})

def upadte_agent(request):
    agt=Utilisateurs.objects.get(id_utilisateur=request.POST['id_agt'])
    user=Utilisateurs.objects.get(id_utilisateur=request.POST['id_user'])
    if request.POST['prenom']:
     agt.prenom = request.POST['prenom']
    if request.POST['nom']:
     agt.email = request.POST['nom']
    if request.POST['telephone']:
     agt.telephone = request.POST['telephone'],

    agt.save()
    return list_agent(request,user.id_utilisateur)
def desactiver_agent(request,id_user,id_agt):
    user=Utilisateurs.objects.get(id_utilisateur=id_user)
    agt=Utilisateurs.objects.get(id_utilisateur=id_agt)
    agt.etat=0
    agt.save()
    return list_agent(request,user.id_utilisateur)
def activer_agent(request,id_user,id_agt):
    user=Utilisateurs.objects.get(id_utilisateur=id_user)
    agt=Utilisateurs.objects.get(id_utilisateur=id_agt)
    agt.etat=1
    agt.save()
    return list_agent(request,user.id_utilisateur)
def reinitiliaser_mdp(request,id_user,id_agt):
    user = Utilisateurs.objects.get(id_utilisateur=id_user)
    agt = Utilisateurs.objects.get(id_utilisateur=id_agt)
    agt.password='reinit'
    agt.save()
    return list_agent(request,user.id_utilisateur)



########Gestion Demande
def demande_acces_boite(request,id,id_boite):
    user=Utilisateurs.objects.get(id_utilisateur=id)
    boite=Boite.objects.get(id_boite=id_boite)
    return render(request, 'templatetra/ajout_demande_boite.html', {'util':user,'boite':boite})
def enregistrer_demande_boite(request):
    dmd=Demande(
        type = 'boite',
        commentaire = request.POST['commentaire'],
         date_dmd = datetime.now(),
        id_demandeur = request.POST['id_user'],
        id_boite = request.POST['id_boite']

    )
    dmd.save()
    return listeboitedirection(request,request.POST['id_user'])

def demande_acces_document(request, id, id_doc):
        user = Utilisateurs.objects.get(id_utilisateur=id)
        doc = Document.objects.get(id_document=id_doc)
        return render(request, 'templatetra/ajout_deamnde_document.html', {'util': user, 'doc': doc})
def enregistrer_demande_doc(request):
    dmd=Demande(
        type = 'document',
        commentaire = request.POST['commentaire'],
         date_dmd = datetime.now(),
        id_demandeur = request.POST['id_user'],
        id_docuement = request.POST['id_doc']

    )
    dmd.save()
    doc=Document.objects.get(id_document=request.POST['id_doc'])
    boite=Boite.objects.get(id_boite=doc.id_boite)
    return listedocumentboite(request,boite.id_boite,request.POST['id_user'])

def refusd_demande_page(request, id, id_dmd):
        user = Utilisateurs.objects.get(id_utilisateur=id)
        dmd = Demande.objects.get(id_dmd=id_dmd)
        return render(request, 'templatetra/refut_dmd.html', {'util': user, 'dmd': dmd})

def enregistrer_demande_refut(request):
    dmd=Demande.objects.get(id_dmd=request.POST['dmd'])
    dmd.commentaire_reponse =request.POST['commentaire']
    dmd.id_accepteur = request.POST['id_user']
    dmd.etat = 2
    dmd.save()
    return listedemesddemandeConsultation(request, request.POST['id_user'])
    #return liste_demande(request, request.POST['id_user'])

def enregistrer_demande_acept(request, id, id_dmd):
    dmd=Demande.objects.get(id_dmd=id_dmd)
    user=Utilisateurs.objects.get(id_utilisateur=id)
    dmd.id_accepteur = id
    dmd.commentaire_reponse='accepté'
    dmd.etat = 1
    dmd.save()
    return listedemesddemandeConsultation(request, id)
    #return liste_demande(request,id)

def liste_demande(request,id):
    user=Utilisateurs.objects.get(id_utilisateur=id)
    dmd=Demande.objects.filter(etat=0)
    lsdmandeur=Utilisateurs.objects.filter(id_utilisateur__in=dmd)
    lsdoc = Document.objects.filter(id_document__in=dmd)
    lsboite = Boite.objects.filter(id_boite__in=dmd)
    restricted_doc_ids = set(lsdoc.values_list('id_document', flat=True))
    restricted_userr_ids = set(lsdmandeur.values_list('id_utilisateur', flat=True))
    restricted_boite_ids = set(lsboite.values_list('id_boite', flat=True))
    for doc in dmd:
        if doc.type== "document" :
           if doc.id_docuement in restricted_doc_ids:

                if doc.id_docuement in restricted_doc_ids:
                    if doc.id_demandeur in restricted_userr_ids:
                        user=Utilisateurs.objects.get(id_utilisateur=doc.id_demandeur)
                        doc.numero = Document.objects.get(id_document=doc).numero_docuemnt
                        doc.user=user.nom + user.prenom
        else :
            if doc.id_boite in restricted_boite_ids:
                if doc.id_demandeur in restricted_userr_ids:
                    user = Utilisateurs.objects.get(id_utilisateur=doc.id_demandeur)
                    doc.numero = Boite.objects.get(id_document=doc).mention
                    doc.user = user.nom + user.prenom


    return render(request, 'templatetra/list_demande.html', {'util':user,'dmd':dmd})

def retriction_page(request, id , id_doc):
    user=Utilisateurs.objects.get(id_utilisateur=id)
    agt=Utilisateurs.objects.filter(direction=user.direction,role='agent')
    doc=Document.objects.get(id_document=id_doc)
    return render(request, 'templatetra/restriction.html', {'util':user,'doc':doc,'agt':agt})

def enregistrer_restriction(request):
    selected_agents = request.POST.getlist('agents')  # Récupère toutes les valeurs sélectionnées
    selected_agents = request.POST.getlist('agt')  # Récupère toutes les valeurs sélectionnées
    for agent_id in selected_agents:
        docu=Document.objects.get(id_document=request.POST['id_doc'])
        boite=Boite.objects.get(id_boite=docu.id_boite)
        user=Utilisateurs.objects.get(id_utilisateur=boite.id_user)
        if not RestrictionDocument.objects.filter(id_doc=request.POST['id_doc'], id_user=agent_id).exists():
            res = RestrictionDocument(
                id_user=agent_id,  # Utilise agent_id directement
                id_doc=request.POST['id_doc'],
                numero_docuent=docu.numero_docuemnt,
                service=user.direction,
                date_dmd=datetime.now(),
                acces=0,
                etat=1
            )
            res.save()
    doc=Document.objects.get(id_document=request.POST['id_doc'])
    return listedocumentboite(request,doc.id_boite,request.POST['id_user'])

def tout_doc(request,id):
    listedoc=Document.objects.all()
    user=Utilisateurs.objects.get(id_utilisateur=id)
    listeuser=Utilisateurs.objects.filter(direction=user.direction)
    boite=Boite.objects.filter(id_user__in=listeuser)
    docuser=Document.objects.filter(id_boite__in=boite)
    listres = RestrictionDocument.objects.filter(id_user=id,etat=1)
    listresdmd = RestrictionDocument.objects.filter(id_user=id, etat=0)

    restricted_doc_ids = set(listres.values_list('id_doc', flat=True))
    list_doc_direction = set(docuser.values_list('id_document', flat=True))
    list_doc_dmd = set(listresdmd .values_list('id_doc', flat=True))
    lst_doc_dmd = Demande.objects.filter(id_demandeur=id)
    restricted_doc_dmd_ids = set(lst_doc_dmd.values_list('id_docuement', flat=True))
    for doc in listedoc:
        ##Consiulataion
        if doc.id_document in restricted_doc_dmd_ids:
            doc.con=0
        else :
            doc.cons=1
            ####direction
        if doc.id_document in list_doc_direction:
            doc.dir=1
        else :
            doc.dir=0
        ######acces
        if doc.id_document in restricted_doc_ids:
                doc.acces = 0
        else :
            doc.acces = 1
        if doc.id_document in list_doc_dmd:
            doc.dmd = 0
        else:
            doc.dmd = 1


    return render(request, 'templatetra/tout_document.html', {'util': user, 'doc': listedoc})

def voir_tout_document(request, id,id_user):
    doc = Document.objects.get(id_document=id)
    user = Utilisateurs.objects.get(id_utilisateur=id_user)
    return render(request, 'templatetra/voir_tout_document.html',
                  {'doc': doc, 'util': user})

##########################################################GESTION  DES CHEF DE SERVICES
def list_chef(request,id):
    listagent = []
    #a = request.session.get('user_id')
    user = Utilisateurs.objects.get(id_utilisateur=id)
    try:
        listagent = Utilisateurs.objects.filter(role='chef')
    except:
        pass
    return render(request, 'templatetra/liste_chef.html', {'chf': listagent, 'user': user, 'util': user})

def Crer_chef_page(request,id):
        forms = UtilisateurForm(request.POST)
        user=Utilisateurs.objects.get(id_utilisateur=id)
        liste = ["facturation", "comptabilité", "documentation", "sacherie", "transfert"
                 , "Document", "Archive"]
        lchef=[]
        all_user=Utilisateurs.objects.filter(role='chef')

        for user in all_user:
                if user.direction in liste:
                    liste.remove(user.direction)

        return render(request, 'templatetra/crer_chef.html', {'forms': forms,'util':user,'all':all_user,'lstdirection':liste})

def enregistrer_chef(request):
    if request.method == 'POST':
        form = UtilisateuwrForm(request.POST)
        user=Utilisateurs.objects.get(id_utilisateur=request.POST["id_user"])
        if form.is_valid() or 1:
            cleaned_data = form.cleaned_data
            instance = Utilisateurs(
                nom=request.POST['nom'],
                prenom=request.POST['prenom'],
                email=request.POST['email'],
                password='chef',
                telephone=request.POST['telephone'],
                direction=request.POST['direction'],
                #direction=user.direction,
                role='chef',

                # form.cleaned_data['direction']
            )
            instance.save()
            #return redirect('/users/login/')
            return list_chef(request,user.id_utilisateur)
        else:
            forms = UtilisateurForm()
            return Crer_chef_page(request, request.POST["id_user"])
            #return render(request, 'templatetra/crer_agent.html', {'forms': forms})

def update_chef_page(request,id_user,id_chf):
    user=Utilisateurs.objects.get(id_utilisateur=id_user)
    agt=Utilisateurs.objects.get(id_utilisateur=id_chf)
    return render(request, 'templatetra/update_agent.html', {'chf':agt,'util':user,'user':agt})

def upadte_chef(request):
    agt=Utilisateurs.objects.get(id_utilisateur=request.POST['id_chf'])
    user=Utilisateurs.objects.get(id_utilisateur=request.POST['id_user'])
    if request.POST['prenom']:
     agt.prenom = request.POST['prenom']
    if request.POST['nom']:
     agt.email = request.POST['nom']
    if request.POST['telephone']:
     agt.telephone = request.POST['telephone'],

    agt.save()
    return list_agent(request,user.id_utilisateur)
def desactiver_chef(request,id_user,id_chf):
    user=Utilisateurs.objects.get(id_utilisateur=id_user)
    agt=Utilisateurs.objects.get(id_utilisateur=id_chf)
    agt.etat=0
    agt.save()
    return list_agent(request,user.id_utilisateur)
def activer_chef(request,id_user,id_chf):
    user=Utilisateurs.objects.get(id_utilisateur=id_user)
    agt=Utilisateurs.objects.get(id_utilisateur=id_chf)
    agt.etat=1
    agt.save()
    return list_agent(request,user.id_utilisateur)
def reinitiliaser_mdp_chef(request,id_user,id_chf):
    user = Utilisateurs.objects.get(id_utilisateur=id_user)
    agt = Utilisateurs.objects.get(id_utilisateur=id_chf)
    agt.password='reinit'
    agt.save()
    return list_agent(request,user.id_utilisateur)


#########Gestion Demande de suppression
def demandepermission(request,id,id_doc,id_boite):
    user=Utilisateurs.objects.get(id_utilisateur=id)
    try:
        doc = RestrictionDocument.objects.get(id_user=id, id_doc=id_doc)

        doc.etat = 0
        doc.save()
        document = Document.objects.get(id_document=doc.id_doc)
        boite = Boite.objects.get(id_boite=document.id_boite)
    except:
        pass

    return listedocumentboite(request,id_boite,user.id_utilisateur)
def acceptr_permission(request,id,id_user):
    res=RestrictionDocument.objects.get(id_restric=id)
    res.delete()
    return listpermission(request,id_user)
def refuser_permission(request,id,id_user):
    res=RestrictionDocument.objects.get(id_restric=id)
    res.etat=3
    res.save()
    return listpermission(request,id_user)


def listpermission(request,id):
    user=Utilisateurs.objects.get(id_utilisateur=id)
    lstuser=Utilisateurs.objects.filter(direction=user.direction)
    listboit=Boite.objects.filter(id_user__in=lstuser)
    listdoc=Document.objects.filter(id_boite__in=listboit)
    Liste_user=Utilisateurs.objects.all()

    lisrect=RestrictionDocument.objects.filter(id_doc__in=listdoc,etat=0)
    restricted_ids_doc = set(listdoc.values_list('id_document', flat=True))
    restricted_ids_user = set(Liste_user.values_list('id_utilisateur', flat=True))

    # Ajouter dynamiquement l'attribut 'acces=0' aux documents restreints dans listedoc
    for doc in lisrect:
        if doc.id_doc in restricted_ids_doc:
            docu=Document.objects.get(id_document=doc.id_doc)
            #doc.document=docu.chemin_acces

            if doc.id_user in restricted_ids_user:
               useru=Utilisateurs.objects.get(id_utilisateur=doc.id_user)
               doc.document = docu.chemin_acces
               doc.numero=docu.numero_docuemnt
               doc.user = useru.prenom+' '+ useru.prenom
    return render(request, 'templatetra/liste_permission.html', {'lstres': lisrect,'util':user})
################Demande Tout

def demande_acces_document_tout(request, id, id_doc):
        user = Utilisateurs.objects.get(id_utilisateur=id)
        doc = Document.objects.get(id_document=id_doc)
        return render(request, 'templatetra/ajouter_demande_tout.html', {'util': user, 'doc': doc})
def enregistrer_demande_doc_tout(request):
    dmd=Demande(
        type = 'document',
        commentaire = request.POST['commentaire'],
         date_dmd = datetime.now(),
        id_demandeur = request.POST['id_user'],
        id_docuement = request.POST['id_doc']

    )
    dmd.save()

    return tout_doc(request,request.POST['id_user'])


def demandepermission_tout(request,id,id_doc):
    user=Utilisateurs.objects.get(id_utilisateur=id)
    try:
        doc = RestrictionDocument.objects.get(id_user=id, id_doc=id_doc)
        doc.etat = 0
        doc.save()
        document = Document.objects.get(id_document=doc.id_doc)
        boite = Boite.objects.get(id_boite=document.id_boite)
    except:
        pass

    return  tout_doc(request,id)
        #listedocumentboite(request,id_boite,user.id_utilisateur)

def voire_document_demande(request, id_user,id_doc):
    doc=Document.objects.get(id_document=id_doc)
    user=Utilisateurs.objects.get(id_utilisateur=id_user)
    return render(request, 'templatetra/voir_demande_document.html',
                  { 'doc': doc,'util':user})



def mes_demandes(request,id):
    user=Utilisateurs.objects.get(id_utilisateur=id)
    res=RestrictionDocument.objects.filter(id_user=id)


    return render(request, 'templatetra/mes_demandes.html', {'lstres': res,'util':user})




########GESTION DES DEMNADES DE CONSULTATIONS
def mes_consultations(request,id):
    dmd=Demande.objects.filter(id_demandeur=id)
    user=Utilisateurs.objects.get(id_utilisateur=id)
    return render(request, 'templatetra/mes_demandes_consultations.html', {'cons': dmd, 'util': user})

######################GESTION DES DEMANDES DE PERMISSION TOUT
def retriction_page_tout(request, id , id_doc):
    user=Utilisateurs.objects.get(id_utilisateur=id)
    agt=Utilisateurs.objects.exclude(id_utilisateur=user.id_utilisateur)
    doc=Document.objects.get(id_document=id_doc)
    return render(request, 'templatetra/restriction_tout.html', {'util':user,'doc':doc,'agt':agt})

def enregistrer_restriction_tout(request):
    selected_agents = request.POST.getlist('agents')  # Récupère toutes les valeurs sélectionnées
    selected_agents = request.POST.getlist('agt')  # Récupère toutes les valeurs sélectionnées
    for agent_id in selected_agents:
        docu=Document.objects.get(id_document=request.POST['id_doc'])
        boite=Boite.objects.get(id_boite=docu.id_boite)
        user=Utilisateurs.objects.get(id_utilisateur=boite.id_user)
        if RestrictionDocument.objects.filter(id_doc=request.POST['id_doc'],id_user=agent_id).exists():
            res = RestrictionDocument(
                id_user=agent_id,  # Utilise agent_id directement
                id_doc=request.POST['id_doc'],
                numero_docuent=docu.numero_docuemnt,
                service=user.direction,
                date_dmd=datetime.now(),
                acces=0,
                etat=1
            )
            res.save()
    doc=Document.objects.get(id_document=request.POST['id_doc'])
    return tout_doc(request,user.id_utilisateur)



def demandepermission_tout(request,id,id_doc):
    user=Utilisateurs.objects.get(id_utilisateur=id)
    try:
        doc = RestrictionDocument.objects.get(id_user=id, id_doc=id_doc)
        doc.etat = 0
        doc.save()
    except:
        pass

    return tout_doc(request,id)

#########################Voir details Consultation
def voir_detail_boite_consultation(request, id,id_user):
    boite=False
    user=False
    try:
      dmd = Demande.objects.get(id_dmd=id)
      boite = Boite.objects.get(id_boite=dmd.id_boite)

    except:
        pass
    user = Utilisateurs.objects.get(id_utilisateur=id_user)
    if boite:
        return render(request, 'templatetra/detail_boite_consultation.html',
                      {'boite': boite, 'user': user, 'util': user})
    else:
        return mes_consultations(request,id_user)

def voir_detail_document_consultation(request, id,id_user):
    boite=False
    doc = False
    user=False
    try:
      dmd=Demande.objects.get(id_dmd=id)
      doc=Document.objects.get(id_document=dmd.id_docuement)
      boite = Boite.objects.get(id_boite=doc.id_boite)

    except:
        pass
    user = Utilisateurs.objects.get(id_utilisateur=id_user)
    if doc:
        return render(request, 'templatetra/detail_document_consultation.html',
                      {'boite': boite,'doc': doc, 'user': user, 'util': user})
    else:
        return mes_consultations(request,id_user)




#def repondre_demande(request,id_user,id_obt):

#######################################Peermisoon non direction
def demandepermission_tout_direction(request,id,id_doc):
    docu=Document.objects.get(id_document=id_doc)
    user=Utilisateurs.objects.get(id_utilisateur=id)
    if RestrictionDocument.objects.filter(id_user=user.id_utilisateur,id_doc=id_doc).exists():
         return tout_doc(request,user.id_utilisateur)
    res = RestrictionDocument(
            id_user=id,  # Utilise agent_id directement
            id_doc=id_doc,
            numero_docuent=docu.numero_docuemnt,
            service=user.direction,
            date_dmd=datetime.now(),
            acces=0,
            etat=0
        )
    res.save()
    #doc=Document.objects.get(id_document=request.POST['id_doc'])
    return tout_doc(request,user.id_utilisateur)








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