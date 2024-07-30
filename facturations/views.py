import doctest
import locale
import os
from datetime import datetime
from tkinter.tix import Form

from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.utils.dateformat import format

from facturations.forms import UtilisateurForm, UtilisateuwrForm, LoginForm, BoiteForm,  DocumentForm
from facturations.models import *


from .decorators import csrf_exempt_all

@csrf_exempt_all
# Create your views here.
def Crer_Utilisateur_page(request):
    forms = UtilisateurForm(request.POST)
    return render(request, 'templatetra/ajout-utilisateur.html', {'forms': forms})
@csrf_exempt
def Deconnexion(request):
    forms = UtilisateurForm(request.POST)
    return render(request, 'templatetra/login1.html', {'forms': forms})


@csrf_exempt
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
                # role=request.POST['rolee']
                role='agent'
                # form.cleaned_data['direction']
            )
            instance.save()
            return redirect('/users/login/')
        else:
            forms = UtilisateurForm()
            return render(request, 'docs/crerutilisateur.html', {'forms': forms})


@csrf_exempt
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
    # a = request.session.get('user_id')
    user = Utilisateurs.objects.get(id_utilisateur=id)
    direction = user.direction
    listuser = Utilisateurs.objects.filter(direction=direction)
    # lst_dt_dmd=Demande.objects.filter(id_demandeur=id,date_retour__isnull=True)
    lst_dt_dmd = Demande.objects.filter(id_demandeur=id, date_retour__isnull=True, etat__in=[0, 1])
    restricted_doc_ids = set(lst_dt_dmd.values_list('id_boite', flat=True))
    try:
        lisboite = Boite.objects.filter(id_user__in=listuser)
        for bt in lisboite:
            if bt.id_boite in restricted_doc_ids:
                bt.cons = 1
            else:
                bt.cons = 0
    except:
        pass
    return render(request, 'templatetra/list_boite.html', {'boite': lisboite, 'user': user, 'util': user})


@csrf_exempt
def ajouterboite_page(request, id):
    forms = BoiteForm()
    # id=request.session.get('user_id')
    user = Utilisateurs.objects.get(id_utilisateur=id)
    # return render(request, 'docs/ajouterboite.html', {'form': forms, 'user': user, 'util': user})
    return render(request, 'templatetra/ajout-boite.html', {'form': forms, 'user': user, 'util': user})


@csrf_exempt
def enregistrerboite(request):
    if request.method == 'POST':
        if Boite.objects.filter(mention=request.POST['mention']).exists():
            user = Utilisateurs.objects.get(id_utilisateur=request.POST['id_user'])
            # return render(request, 'docs/ajouterboite.html', {'form': forms, 'user': user, 'util': user})
            return render(request, 'templatetra/ajout-boite.html', { 'user': user, 'util': user,'message' : 'La boîte mentionnée existe déjà !'})


        #return ajouterboite_page(request, request.POST['id_user'])
            # cleaned_data = form.cleaned_data
        else:
            instance = Boite(
                mention=request.POST['mention'],
                date_creation=datetime.now(),
                id_user=request.POST['id_user']
            )
            instance.save()
            # listeboitedirection(request, request.POST['id_user'])

            return redirect("/doc/listeboite/" + str(request.POST['id_user']))

    else:

        # return ajouterboite_page(request, request.POST['id_user'])
        return redirect("/doc/jouterboite_page/" + str(request.POST['id_user']))


@csrf_exempt
def listedocumentboite(request, id, id_user):
    listedoc = []
    boite = False
    listres = RestrictionDocument.objects.filter(id_user=id_user)
    lst_bt_dmd = Demande.objects.filter(id_boite=id)
    doc_bt_dmd = Document.objects.filter(id_boite__in=lst_bt_dmd)
    #####Document boite en cours
    doc_bt = Document.objects.filter(id_boite=id)
    bt_dmd = Document.objects.filter(id_boite=id)
    doc_bt_dmd_crs = Document.objects.filter(id_boite__in=bt_dmd)
    user = False
    lisboite = Boite.objects.exclude(numero_rang__startswith='Auc')

    try:
        listedoc = Document.objects.filter(id_boite=id)

        boite = Boite.objects.get(id_boite=id)

    except:
        pass
    ###liste des documents restraintre
    restricted_doc_ids = set(listres.values_list('id_doc', flat=True))
    restricted_doc_bt__ids = set(doc_bt_dmd.values_list('id_document', flat=True))
    restricted_bt_crs_ids = set(doc_bt_dmd_crs.values_list('id_boite', flat=True))
    lst_doc_dmd = Demande.objects.filter(id_demandeur=id_user)
    restricted_doc_dmd_ids = set(lst_doc_dmd.values_list('id_docuement', flat=True))
    bt_dmd = Demande.objects.filter(id_boite=id)
    bt_dmd_ids = set(bt_dmd.values_list('id_boite', flat=True))
    listedoc = Document.objects.filter(id_boite=id)

    # Ajouter dynamiquement l'attribut 'acces=0' aux documents restreints dans listedoc

    for doc in listedoc:

        if Demande.objects.filter(id_boite=id).exists():
            doc.bt = 1
        else:
            doc.bt = 0
        if Demande.objects.filter(id_docuement=doc.id_document, id_demandeur=id_user, date_retour__isnull=True,
                                  etat__in=[0, 1]).exists():
            doc.cons = 1
        else:
            doc.cons = 0

        if doc.id_document in restricted_doc_bt__ids:
            doc.disp = 0
        else:
            doc.disp = 1

        if doc.id_document in restricted_doc_ids:
            docres = RestrictionDocument.objects.get(id_doc=doc.id_document, id_user=id_user)
            doc.ref = docres.ref
            doc.dmd = docres.dmd
            doc.acces = 0
            doc.etat = 1
        else:
            doc.acces = 1

    user = Utilisateurs.objects.get(id_utilisateur=id_user)
    return render(request, 'templatetra/list_document_agent.html',
                  {'doc': listedoc, 'user': user, 'util': user, 'boite': boite})


@csrf_exempt
def clotureBoite(request, id):
    boite = False
    user = False
    try:
        boite = Boite.objects.get(id_boite=id)
        boite.etat = 0
        boite.save()

    except:
        pass
    user = Utilisateurs.objects.get(id_utilisateur=boite.id_user)
    if boite:
        return listeboitedirection(request, user.id_utilisateur)

    # return listedocumentboite(request, id)
    return redirect("/doc/listeboite/" + str(id))


@csrf_exempt
def voir_detail_boite(request, id, id_user):
    boite = False
    user = False
    try:
        boite = Boite.objects.get(id_boite=id)

    except:
        pass
    user = Utilisateurs.objects.get(id_utilisateur=id_user)
    if boite:
        return render(request, 'templatetra/detail_boite.html',
                      {'boite': boite, 'user': user, 'util': user})
    else:
        # return listeboitedirection(request, user.id_utilisateur)
        return redirect("/doc/listeboite/" + str(user.id_utilisateur))


@csrf_exempt
def updateboite(request):
    boite = False
    user = False
    try:
        boite = Boite.objects.get(id_boite=request.POST['id_boite'])

    except:
        pass
    user = Utilisateurs.objects.get(id_utilisateur=request.POST['id_user'])
    if boite:
        boite_ex=Boite.objects.exclude(id_boite=request.POST['id_boite'])
        if boite_ex.filter(mention=request.POST['mention']).exists() :
            return render(request, 'templatetra/detail_boite.html',
                          {'boite': boite, 'user': user, 'util': user,'message' : 'la mention de la boite existe déja'})
        boite.mention = request.POST['mention']
        boite.save()
        return listeboitedirection(request, user.id_utilisateur)
    else:
        return voir_detail_boite(request, boite.id_boite)


@csrf_exempt
def voire_document(request, id, id_user):
    doc = Document.objects.get(id_document=id)
    user = Utilisateurs.objects.get(id_utilisateur=id_user)
    return render(request, 'templatetra/voir_document.html',
                  {'doc': doc, 'util': user})

    ####################################################################GESTION DOCUMENT############################################


@csrf_exempt
def ajouterdossier_page(request, id):
    forms = DocumentForm()
    boite = Boite.objects.get(id_boite=id)
    user = Utilisateurs.objects.get(id_utilisateur=boite.id_user)
    # return render(request, 'docs/ajouerterdossier.html', {'form': forms, 'user': user, 'util': user, 'boite': boite})
    return render(request, 'templatetra/ajout-document.html',
                  {'form': forms, 'user': user, 'util': user, 'boite': boite})


@csrf_exempt
def ajouterdocumentboite(request):
    if request.method == 'POST':
        form = BoiteForm(request.POST)
        user = False
        boite = False
        try:
            user = Utilisateurs.objects.get(id_utilisateur=request.POST['id_user'])
            boite = Boite.objects.get(id_boite=request.POST['id_boite'])
        except:
            pass
        fichier = request.FILES['file']
        handle_uploaded_file(fichier)
        current_timestamp = int(datetime.timestamp(datetime.now()))
        if form.is_valid() or 1:


            # derniere_per = Permission.objects.latest(' id_permission')
            ####Ajoter Document
            if Document.objects.filter(numero_docuemnt=request.POST['numero']).exists() or Document.objects.filter(bl=request.POST['bl']).exists():
                message = ''
                messagebl = ''
                if Document.objects.filter(numero_docuemnt=request.POST['numero']).exists():
                    message = 'L\'identifiant mentionné existe deja'
                if Document.objects.filter(bl=request.POST['bl']).exists():
                    messagebl= 'Le BL mentionné exite déja'
                return render(request, 'templatetra/ajout-document.html',
                              { 'user': user, 'util': user, 'boite': boite,'message': message, 'messagebl': messagebl})
                #return ajouterdossier_page(request, request.POST['id_boite'])

                #return ajouterdossier_page(request, request.POST['id_boite'])
            instance = Document(numero_docuemnt=request.POST['numero'],
                                date_creation=datetime.now(),
                                chemin_acces=str(current_timestamp) + fichier.name,
                                eta=request.POST['eta'],
                                bl=request.POST['bl'],
                                client=request.POST['client'],
                                nom_navire=request.POST['navire'],
                                numero_voyage=request.POST['voyage'],
                                id_boite=request.POST['id_boite'],
                                id_per=2
                                )
            instance.save()
            return  redirect("/doc/listedocumentboite/" + str(request.POST['id_boite'])+ "/" + str(request.POST['id_user']))

            #return listedocumentboite(request, request.POST['id_boite'], request.POST['id_user'])
    else:
        forms = DocumentForm()
        boite = Boite.objects.get(id_boite=request.POST['boite'])
        user = Utilisateurs.objects.get(id_user=boite.id_user)
        return render(request, 'docs/ajouerterdossier.html',
                      {'forms': forms, 'user': user, 'util': user, 'boiie': boite})


@csrf_exempt
def handle_uploaded_file(f):
    current_timestamp = int(datetime.timestamp(datetime.now()))
    with open('static/archives/' + str(current_timestamp) + f.name, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)


@csrf_exempt


def voir_document(request, id_document):
    fichier_pdf = Document.objects.get(id_document=id_document)
    boite = Boite.objects.get(id_boite=fichier_pdf.id_boite)
    user = Utilisateurs.objects.get(id_user=request.session.get('id_user'))
    return render(request, 'docs/voirfichier.html',
                  {'doc': fichier_pdf, 'user': fichier_pdf.id_user, 'util': user, 'boite': boite})


##################ajouter detail##################################################################
####Gestion demande#######################################
@csrf_exempt
def listedemesddemandeConsultation(request, id):
    listdmd = []
    a = request.session.get('user_id')
    user = Utilisateurs.objects.get(id_utilisateur=id)
    try:
        # listdmd = Demande.objects.filter(id_demandeur=id)
        listdmd = Demande.objects.filter(etat=0)
    except:
        pass
    lst_doc = Document.objects.all()
    # lst_user=Utilisateurs.objects.all()
    lst_boite = Boite.objects.all()
    restricted_boite_ids = set(lst_boite.values_list('id_boite', flat=True))
    restricted_doc_ids = set(lst_doc.values_list('id_document', flat=True))
    # restricted_user_ids = set(lst_boite.values_list('id_utilisateur', flat=True))
    for doc in listdmd:
        if doc.type == "document":
            doc.bt = 0
            if doc.id_docuement in restricted_doc_ids:
                docu = Document.objects.get(id_document=doc.id_docuement)
                doc.numero = docu.numero_docuemnt

                user = Utilisateurs.objects.get(id_utilisateur=doc.id_demandeur)
                doc.user = user.nom + ' ' + user.prenom
        else:
            doc.bt = 1
            if doc.id_boite in restricted_boite_ids:
                boite = Boite.objects.get(id_boite=doc.id_boite)
                doc.numero = boite.mention
                doc.id_docuement = ''
                doc.id_boite = boite.id_boite
                user = Utilisateurs.objects.get(id_utilisateur=doc.id_demandeur)
                doc.user = user.nom + ' ' + user.prenom

    return render(request, 'templatetra/list_demande.html', {'dmd': listdmd, 'user': user, 'util': user})


@csrf_exempt
def ajouterdemande_page(request, id, idobj):
    # forms = DemandeForm()
    # id=request.session.get('user_id')
    user = Utilisateurs.objects.get(id_user=id)
    boite = False
    try:
        boite = Boite.objects.get(id_boite=idobj)
    except:
        pass
    # 'form': forms,
    return render(request, 'docs/ajouterboite.html', {'user': user, 'util': user, 'boite': boite})


@csrf_exempt
def ajouterdemande(request):
    if request.method == 'POST':
        form = BoiteForm(request.POST)
        id_user = request.session.get('user_id')
        locale.setlocale(locale.LC_TIME, 'fr_FR.UTF-8')
        now = datetime.now()
        formatted_now = now.strftime("%d %B %Y %H:%M:%S")
        type = 'document'
        if request.POST['boite']:
            type = 'boite'
        if form.is_valid() or 1:
            instance = Demande(
                type=type,
                commentaire=request.POST['comentaire'],
                date_dmd=datetime.now(),
                # date_retour =,

                id_demandeur=request.POST['id_user'],
                # id_accepteur = ,
                etat=0,
                id_docuement=request.POST['id_document'],
                id_boite=request.POST['id_boite'],

            )
            instance.save()
            return listedemesddemande(request, request.POST['id_user'])

    else:
        return ajouterdemande_page(request, request.POST['id_user'])


@csrf_exempt
def listedemanddeencour(request, id):
    listdmd = []
    a = request.session.get('user_id')
    user = Utilisateurs.objects.get(id_user=id)
    try:
        listdmd = Demande.objects.filter(etat=0)
    except:
        pass
    return render(request, 'docs/listeboite.html', {'dmd': listdmd, 'user': user, 'util': user})


@csrf_exempt
def accepterdemande_page(request, id, id_user):
    # forms = DemandeForm()
    # id=request.session.get('user_id')
    user = Utilisateurs.objects.get(id_user=id_user)
    dmd = Demande.objects.get(id_dmd__gte=id)
    # 'form': forms,
    return render(request, 'docs/ajouterboite.html', {'user': user, 'util': user, 'dmd': dmd})


@csrf_exempt
def refuserdemande_page(request, id, id_user):
    # forms = DemandeForm()
    # id=request.session.get('user_id')
    user = Utilisateurs.objects.get(id_user=id_user)
    dmd = Demande.objects.get(id_dmd__gte=id)
    # 'form': forms,
    return render(request, 'docs/ajouterboite.html', {'user': user, 'util': user, 'dmd': dmd})


@csrf_exempt
def accepterdeamnde(request):
    if request.method == 'POST':
        # etat passe a 1
        dmd = Demande.objects.get(id_dmd=request.POST['id_dmd'])
        dmd.id_accepteur = 'ok'
        dmd.commentaire_reponse = request.POST['rescom']
        dmd.eta = 1
        dmd.save()
        return listedemanddeencour(request, dmd.id_demandeur)


@csrf_exempt
def refusedemande(request, id, id_user):
    if request.method == 'POST':
        dmd = Demande.objects.get(id_dmd=request.POST['id_dmd'])
        dmd.id_accepteur = id_user
        dmd.id_accepteur = request.POST['id_use']
        dmd.commentaire_reponse = request.POST['rescom']
        dmd.etat = 2
        dmd.save()
        return listedemanddeencour(request, dmd.id_demandeur)


###############################################Archiviste######################################################################
@csrf_exempt
def listeboiteAclasser(request, id):
    boite = Boite.objects.filter(etat=0, numero_rang__startswith='Aucune')
    user = Utilisateurs.objects.get(id_utilisateur=id)
    # return render(request, 'docs/listeboiteclasser.html', {'doc': boite, 'user': user, 'util': user})

    return render(request, 'templatetra/liste_boite_cloture.html', {'boite': boite, 'user': user, 'util': user})


@csrf_exempt
def classerBoite_page(request, id, id_user):
    boite = Boite.objects.get(id_boite=id)
    user = Utilisateurs.objects.get(id_utilisateur=id_user)
    return render(request, 'templatetra/classer_boite.html',
                  {'user': user, 'util': user, 'boite': boite})


@csrf_exempt
def classerboite(request):
    if request.method == 'POST':
        id = request.POST['id_user']
        id_boite = request.POST['id_boite']
        id_user = request.POST['id_user']
        if  Boite.objects.filter(numero_rang=request.POST['numerorang']).exists():
            boite = Boite.objects.get(id_boite=id_boite)
            user = Utilisateurs.objects.get(id_utilisateur=id_user)
            return render(request, 'templatetra/classer_boite.html',
                          {'user': user, 'util': user, 'boite': boite,'message':'Ce numero de rangement existe déjà!'})
        else:
            boit = Boite.objects.get(id_boite=id_boite)
            boit.numero_rang = request.POST['numerorang']
            boit.harmoire = request.POST['armoire']
            boit.numero_comp = request.POST['com']
            boit.niveau = request.POST['niveau']
            # boit.etat=1
            boit.save()
            return redirect("/doc/liste_boite_classes/" + str(request.POST['id_user']))

            # return listeboiteclasser(request, request.POST['id_user'])
    else:

            return redirect(
                "/doc/liste_boite_classer/" + str(request.POST['id_boite']) + "/" + str(request.POST['id_user']))
            # return classerBoite_page(request, request.POST['id_user'])


@csrf_exempt
def listeboiteclasser(request, id):
    lisboite = []
    user = Utilisateurs.objects.get(id_utilisateur=id)
    try:
        lisboite = Boite.objects.exclude(numero_rang__startswith='Auc')
    except:
        pass
    #loc = Localisation.objects.all()
    return render(request, 'templatetra/liste_boite_classer.html',
                  {'boite': lisboite, 'user': user, 'util': user})


@csrf_exempt
def voir_detail_archive(request, id, id_user):
    boite = Boite.objects.get(id_boite=id)
    user = Utilisateurs.objects.get(id_utilisateur=id_user)
    return render(request, 'templatetra/detail_archiviste.html', {'boite': boite, 'user': user, 'util': user})


@csrf_exempt
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
            boite_ex = Boite.objects.exclude(id_boite=request.POST['id_boite'])
            if boite_ex.filter(numero_rang=request.POST['numero_rang']).exists():
                return render(request, 'templatetra/detail_archiviste.html',
                              {'boite': boit, 'user': user, 'util': user,
                               'message': 'le numero de rangement de la boite existe déja'})
            boit.numero_rang = request.POST['numero_rang']
        boit.harmoire = request.POST['armoire']
        if request.POST['armoire']:
            boit.harmoire = request.POST['armoire']

        if request.POST['com']:
            boit.numero_comp = request.POST['com']
        if request.POST['niveau']:
            boit.niveau = request.POST['niveau']
        boit.save()
        # return listeboiteclasser(request, user.id_utilisateur)
        return redirect("/doc/liste_boite_classes/" + str(user.id_utilisateur))

    else:
        return redirect("/doc/detail_boite/" + str(boit.id_boite) + "/" + str(user.id_utilisateur))

        # return voir_detail_archive(request, boit.id_boite,user.id_utilisateur)


###########################################################Gestion demnade Permission
@csrf_exempt
def demandepermission_page(request, id, id_user):
    doc = Document.objects.get(id_document=id)
    user = Utilisateurs.objects.get(id_user=id_user)
    return render(request, 'docs/ajouterdossierarchiviste.html',
                  {'user': user, 'util': user, 'doc': doc})




###########################GESTION EQUIPE
@csrf_exempt
def list_agent(request, id):
    listagent = []
    # a = request.session.get('user_id')
    user = Utilisateurs.objects.get(id_utilisateur=id)
    try:
        listagent = Utilisateurs.objects.filter(role='agent', direction=user.direction)
    except:
        pass
    return render(request, 'templatetra/list_agent.html', {'agt': listagent, 'user': user, 'util': user})


@csrf_exempt
def Crer_agent_page(request, id):
    forms = UtilisateurForm(request.POST)
    user = Utilisateurs.objects.get(id_utilisateur=id)
    return render(request, 'templatetra/crer_agent.html', {'forms': forms, 'util': user})


@csrf_exempt
def enregistrer_agent(request):
    if request.method == 'POST':
        form = UtilisateuwrForm(request.POST)
        user = Utilisateurs.objects.get(id_utilisateur=request.POST["id_user"])
        check_email = Utilisateurs.objects.filter(email=request.POST['email'])
        if check_email:

            message = 'Cet email est déjà utilisé par un autre utilisateur.'
            return render(request, 'templatetra/crer_agent.html',
                          {'util': user, 'message': message})
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
                # role=request.POST['rolee']
                role='agent'
                # form.cleaned_data['direction']
            )
            instance.save()
            # return redirect('/users/login/')
            return list_agent(request, user.id_utilisateur)
        else:
            forms = UtilisateurForm()
            return Crer_agent_page(request, request.POST["id_user"])
            # return render(request, 'templatetra/crer_agent.html', {'forms': forms})


@csrf_exempt
def update_agent_page(request, id_user, id_agt):
    user = Utilisateurs.objects.get(id_utilisateur=id_user)
    agt = Utilisateurs.objects.get(id_utilisateur=id_agt)
    return render(request, 'templatetra/update_agent.html', {'agt': agt, 'util': user, 'user': agt})
@csrf_exempt
def upadte_agent(request):
    agt = Utilisateurs.objects.get(id_utilisateur=request.POST['id_agt'])
    # Récupérer l'utilisateur qui effectue la mise à jour
    user = Utilisateurs.objects.get(id_utilisateur=request.POST['id_user'])
    # Mettre à jour les champs selon les données reçues en POST
    if request.POST.get('prenom'):
        agt.prenom = request.POST['prenom']

    if request.POST.get('nom'):
        agt.nom = request.POST['nom']

    if request.POST.get('email'):
        # Vérifier si l'email est déjà utilisé par un autre utilisateur
        if agt.email != request.POST['email'] and Utilisateurs.objects.filter(email=request.POST['email']).exclude(
                id_utilisateur=agt.id_utilisateur).exists():
            message = 'Cet email est déjà utilisé par un autre utilisateur.'
            return render(request, 'templatetra/update_agent.html', {'agt': agt, 'util': user, 'message': message})
        else:
            agt.email = request.POST['email']

    if request.POST.get('telephone'):
        agt.telephone = request.POST['telephone']

    # Sauvegarder les modifications dans la base de données
    agt.save()
    return list_agent(request, user.id_utilisateur)


@csrf_exempt
def desactiver_agent(request, id_user, id_agt):
    user = Utilisateurs.objects.get(id_utilisateur=id_user)
    agt = Utilisateurs.objects.get(id_utilisateur=id_agt)
    agt.etat = 0
    agt.save()
    return list_agent(request, user.id_utilisateur)


@csrf_exempt
def activer_agent(request, id_user, id_agt):
    user = Utilisateurs.objects.get(id_utilisateur=id_user)
    agt = Utilisateurs.objects.get(id_utilisateur=id_agt)
    agt.etat = 1
    agt.save()
    return list_agent(request, user.id_utilisateur)


@csrf_exempt
def reinitiliaser_mdp(request, id_user, id_agt):
    user = Utilisateurs.objects.get(id_utilisateur=id_user)
    agt = Utilisateurs.objects.get(id_utilisateur=id_agt)
    agt.password = '1234'
    agt.save()
    return list_agent(request, user.id_utilisateur)


########Gestion Demande
@csrf_exempt
def demande_acces_boite(request, id, id_boite):
    user = Utilisateurs.objects.get(id_utilisateur=id)
    boite = Boite.objects.get(id_boite=id_boite)
    return render(request, 'templatetra/ajout_demande_boite.html', {'util': user, 'boite': boite})


@csrf_exempt
def enregistrer_demande_boite(request):
    #########A refaire
    dmd = Demande(
        type='boite',
        commentaire=request.POST['commentaire'],
        date_dmd=datetime.now(),
        id_demandeur=request.POST['id_user'],
        id_boite=request.POST['id_boite']

    )
    dmd.save()
    return redirect("/doc/listeboite/" + str(request.POST['id_user']))
    # return listeboitedirection(request,request.POST['id_user'])


@csrf_exempt
def demande_acces_document(request, id, id_doc):
    user = Utilisateurs.objects.get(id_utilisateur=id)
    doc = Document.objects.get(id_document=id_doc)
    return render(request, 'templatetra/ajout_deamnde_document.html', {'util': user, 'doc': doc})


@csrf_exempt
def enregistrer_demande_doc(request):
    dmd = Demande(
        type='document',
        commentaire=request.POST['commentaire'],
        date_dmd=datetime.now(),
        id_demandeur=request.POST['id_user'],
        id_docuement=request.POST['id_doc']

    )
    dmd.save()
    doc = Document.objects.get(id_document=request.POST['id_doc'])
    boite = Boite.objects.get(id_boite=doc.id_boite)
    return redirect("/doc/listedocumentboite/" + str(boite.id_boite) + "/" + str(request.POST['id_user']))
    # return listedocumentboite(request,boite.id_boite,request.POST['id_user'])


@csrf_exempt
def refusd_demande_page(request, id, id_dmd):
    user = Utilisateurs.objects.get(id_utilisateur=id)
    dmd = Demande.objects.get(id_dmd=id_dmd)
    return render(request, 'templatetra/refut_dmd.html', {'util': user, 'dmd': dmd})


@csrf_exempt
def enregistrer_demande_refut(request):
    dmd = Demande.objects.get(id_dmd=request.POST['dmd'])
    dmd.commentaire_reponse = request.POST['commentaire']
    dmd.id_accepteur = request.POST['id_user']
    dmd.etat = 2
    dmd.save()
    return redirect("/doc/listedmd/" + str(request.POST['id_user']))
    # return listedemesddemandeConsultation(request, request.POST['id_user'])
    # return liste_demande(request, request.POST['id_user'])


@csrf_exempt
def enregistrer_demande_acept(request, id, id_dmd):
    dmd = Demande.objects.get(id_dmd=id_dmd)
    user = Utilisateurs.objects.get(id_utilisateur=id)
    dmd.id_accepteur = id
    dmd.commentaire_reponse = 'accepté'
    dmd.etat = 1
    dmd.save()
    return redirect("/doc/listedmd/" + str(id))


@csrf_exempt
def enregistrer_retour(request, id, id_dmd):
    dmd = Demande.objects.get(id_dmd=id_dmd)
    user = Utilisateurs.objects.get(id_utilisateur=id)
    dmd.id_accepteur = id
    dmd.commentaire_reponse = 'accepté'
    dmd.date_retour = datetime.now()
    dmd.save()
    return redirect("/doc/listedmd/" + str(id))


# return listedemesddemandeConsultation(request, id)
# return liste_demande(request,id)

@csrf_exempt
def liste_demande(request, id):
    user = Utilisateurs.objects.get(id_utilisateur=id)
    dmd = Demande.objects.filter(date_retour__isnull=True, etat__in=[0, 1])
    lsdmandeur = Utilisateurs.objects.filter(id_utilisateur__in=dmd)
    lsdoc = Document.objects.filter(id_document__in=dmd)
    lsboite = Boite.objects.filter(id_boite__in=dmd)
    restricted_doc_ids = set(lsdoc.values_list('id_document', flat=True))
    restricted_userr_ids = set(lsdmandeur.values_list('id_utilisateur', flat=True))
    restricted_boite_ids = set(lsboite.values_list('id_boite', flat=True))
    ###retour
    dmd_accepte = Demande.objects.filter(etat=1, date_retour__isnull=True)
    dmd_accepte_ids = set(dmd_accepte.values_list('id_dmd', flat=True))
    #####Accepter
    # dmd_attente = Demande.objects.filter(id_accepteur__isnull=True)
    # dmd_attente_ids = set(dmd_attente.values_list('id_dmd', flat=True))
    for doc in dmd:
        if doc.id_dmd in dmd_accepte_ids:
            doc.ret = 1
        else:
            doc.ret = 0

        if doc.type == "document":
            doc.bt = 0
            user = Utilisateurs.objects.get(id_utilisateur=doc.id_demandeur)
            doc.numero = Document.objects.get(id_document=doc.id_docuement).numero_docuemnt
            doc.user = user.nom + user.prenom
            dmd_attente_boite = Demande.objects.filter(date_retour__isnull=True, etat=1, id_docuement=doc.id_docuement)
            dmd_attente_boite_ids = set(dmd_attente_boite.values_list('id_docuement', flat=True))
            if doc.id_docuement in dmd_attente_boite_ids:
                doc.att = 1
            else:
                doc.att = 0
            if doc.id_docuement in restricted_doc_ids:
                dmd_attente_boite = Demande.objects.filter(date_retour__isnull=True, etat=1,
                                                           id_docuement=doc.id_docuement)
                dmd_attente_boite_ids = set(dmd_attente_boite.values_list('id_docuement', flat=True))
                if doc.id_docuement in dmd_attente_boite_ids:
                    doc.att = 1
                else:
                    doc.att = 0

                if doc.id_docuement in restricted_doc_ids:
                    if doc.id_demandeur in restricted_userr_ids:
                        user = Utilisateurs.objects.get(id_utilisateur=doc.id_demandeur)
                        doc.numero = Document.objects.get(id_document=doc).numero_docuemnt
                        doc.user = user.nom + user.prenom
        else:
            doc.bt = 1
            user = Utilisateurs.objects.get(id_utilisateur=doc.id_demandeur)
            doc.numero = Boite.objects.get(id_boite=doc.id_boite).mention
            doc.user = user.nom + user.prenom
            dmd_attente_boite = Demande.objects.filter(date_retour__isnull=True, etat=1, id_boite=doc.id_boite)
            dmd_attente_boite_ids = set(dmd_attente_boite.values_list('id_boite', flat=True))
            if doc.id_boite in dmd_attente_boite_ids:
                doc.att = 1
            else:
                doc.att = 0
            if doc.id_boite in restricted_boite_ids:
                user = Utilisateurs.objects.get(id_utilisateur=doc.id_demandeur)
                doc.numero = Boite.objects.get(id_boite=doc.id_boite).mention
                doc.user = user.nom + user.prenom
                if doc.id_demandeur in restricted_userr_ids:
                    user = Utilisateurs.objects.get(id_utilisateur=doc.id_demandeur)
                    doc.numero = Boite.objects.get(id_boite=doc.id_boite).mention
                    doc.user = user.nom + user.prenom

    useru = Utilisateurs.objects.get(id_utilisateur=id)
    return render(request, 'templatetra/list_demande.html', {'util': useru, 'dmd': dmd})




@csrf_exempt
def retriction_page(request, id, id_doc):
    user = Utilisateurs.objects.get(id_utilisateur=id)
    agt = Utilisateurs.objects.filter(direction=user.direction, role='agent')
    res_doc = RestrictionDocument.objects.filter(id_doc=id_doc)

    res_doc_acces = RestrictionDocument.objects.filter(id_doc=id_doc, acces_dir=3)
    rgbt_ids = set(res_doc_acces.values_list('id_user', flat=True))
    agt_acces= Utilisateurs.objects.filter(id_utilisateur__in=rgbt_ids)


    agt = Utilisateurs.objects.filter(direction=user.direction).exclude(id_utilisateur=user.id_utilisateur).union(agt_acces)

    #agt = Utilisateurs.objects.filter(direction=user.direction).exclude(id_utilisateur=user.id_utilisateur)
    for agent_id in res_doc:
        # agt.exclude(id_utilisateur=agent_id.id_user)
        # agt.filter(id_utilisateur=agent_id.id_user).delete()
        agt = [agent for agent in agt if agent.id_utilisateur != agent_id.id_user  ]
    doc = Document.objects.get(id_document=id_doc)

    doc = Document.objects.get(id_document=id_doc)
    agt_dir = Utilisateurs.objects.filter(id_utilisateur__in=rgbt_ids)

    return render(request, 'templatetra/restriction.html', {'util': user, 'doc': doc, 'agt': agt , 'agt_dir': agt_dir})

@csrf_exempt
def enregistrer_restriction(request):
    selected_agents = request.POST.getlist('agents')  # Récupère toutes les valeurs sélectionnées
    selected_agents = request.POST.getlist('agt')  # Récupère toutes les valeurs sélectionnées
    util = Utilisateurs.objects.get(id_utilisateur=request.POST['id_user'])
    for agent_id in selected_agents:
        docu = Document.objects.get(id_document=request.POST['id_doc'])
        boite = Boite.objects.get(id_boite=docu.id_boite)
        user = Utilisateurs.objects.get(id_utilisateur=boite.id_user)
        user_crt = Utilisateurs.objects.get(id_utilisateur=agent_id)
        if user_crt.direction == util.direction:
            if not RestrictionDocument.objects.filter(id_doc=request.POST['id_doc'], id_user=agent_id).exists():
                res = RestrictionDocument(
                    id_user=agent_id,  # Utilise agent_id directement
                    id_doc=request.POST['id_doc'],
                    numero_docuent=docu.numero_docuemnt,
                    service=user.direction,
                    date_dmd=datetime.now(),
                    acces=0,
                    etat=1,
                    id_chef=request.POST['id_user']
                )
                res.save()
        else:

                RestrictionDocument.objects.filter(id_doc=request.POST['id_doc'], id_user=agent_id).delete()

    doc = Document.objects.get(id_document=request.POST['id_doc'])
    return redirect("/doc/listedocumentboite/" + str(doc.id_boite) +"/"+str(request.POST['id_user']))
    #return listedocumentboite(request, doc.id_boite, request.POST['id_user'])

@csrf_exempt
def tout_doc(request, id):
    # listedoc=Document.objects.all()
    listedoc = Document.objects.exclude(numero_docuemnt__startswith='CAT')
    user = Utilisateurs.objects.get(id_utilisateur=id)
    listeuser = Utilisateurs.objects.filter(direction=user.direction)
    boite = Boite.objects.filter(id_user__in=listeuser)
    ####document meeme direction
    docuser = Document.objects.filter(id_boite__in=boite)
    #####liste des documents restreintre
    listres = RestrictionDocument.objects.filter(id_user=id)
    ###############Liste des Docuemnts
    listresdmd = RestrictionDocument.objects.filter(id_user=id, etat=0)

    restricted_doc_ids = set(listres.values_list('id_doc', flat=True))
    list_doc_direction = set(docuser.values_list('id_document', flat=True))
    list_doc_dmd = set(listresdmd.values_list('id_doc', flat=True))
    lst_doc_dmd = Demande.objects.filter(id_demandeur=id)
    restricted_doc_dmd_ids = set(lst_doc_dmd.values_list('id_docuement', flat=True))
    ######boite  ranger
    lisboite_rg = Boite.objects.exclude(numero_rang__startswith='Auc')
    boite_range = set(lisboite_rg.values_list('id_boite', flat=True))
    ######boit occupe
    ######doc occupe
    lisboite_occupe = Demande.objects.filter(id_demandeur=id, etat__in=[0, 1], date_retour__isnull=True)
    doc_occupe = set(lisboite_occupe.values_list('id_docuement', flat=True))
    # Ajouter dynamiquement l'attribut 'acces=0' aux documents restreints dans listedoc

    for doc in listedoc:
        if doc.id_document in doc_occupe:
            doc.occ = 1
        else:
            doc.occ = 0

        if doc.id_boite in boite_range:
            doc.rg = 1
        else:
            doc.rg = 0
        if doc.id_document in restricted_doc_dmd_ids:
            doc.cons = 0
        else:
            doc.cons = 1
        if doc.id_document in list_doc_direction:
            doc.dir = 1

        else:
            doc.dir = 0
            doc.per = 1

        if doc.id_document in restricted_doc_ids:
            docres = RestrictionDocument.objects.get(id_doc=doc.id_document, id_user=id)
            doc.ref = docres.ref
            doc.dmd = docres.dmd
            doc.accept_dir = docres.acces_dir
            doc.acces = 0
            doc.etat = 1
            doc.per = 0
        else:
            doc.acces = 1
            doc.per = 1

    user = Utilisateurs.objects.get(id_utilisateur=id)

    return render(request, 'templatetra/tout_document.html', {'util': user, 'doc': listedoc})

@csrf_exempt
def voir_tout_document(request, id, id_user):
    doc = Document.objects.get(id_document=id)
    user = Utilisateurs.objects.get(id_utilisateur=id_user)
    return render(request, 'templatetra/voir_tout_document.html',
                  {'doc': doc, 'util': user})


##########################################################GESTION  DES CHEF DE SERVICES
@csrf_exempt
def list_chef(request, id):
    listagent = []
    # a = request.session.get('user_id')
    user = Utilisateurs.objects.get(id_utilisateur=id)
    try:
        listagent = Utilisateurs.objects.filter(role='chef')
    except:
        pass
    return render(request, 'templatetra/liste_chef.html', {'chf': listagent, 'user': user, 'util': user})


@csrf_exempt
def Crer_chef_page(request, id):
    forms = UtilisateurForm(request.POST)
    user = Utilisateurs.objects.get(id_utilisateur=id)
    liste = ["facturation", "comptabilité", "documentation", "sacherie", "transfert"
        ,  "archive"]
    lchef = []
    all_user = Utilisateurs.objects.filter(role='chef')

    for user1 in all_user  :
        if user1.direction in liste:
            liste.remove(user1.direction)

    return render(request, 'templatetra/crer_chef.html',
                  {'forms': forms, 'util': user, 'all': all_user, 'lstdirection': liste})


@csrf_exempt
def enregistrer_chef(request):
    if request.method == 'POST':
        form = UtilisateuwrForm(request.POST)
        user = Utilisateurs.objects.get(id_utilisateur=request.POST["id_user"])
        check_email = Utilisateurs.objects.filter(email=request.POST['email']).exclude(
            id_utilisateur=user.id_utilisateur).exists()
        if check_email:
            all_user = Utilisateurs.objects.filter(role='chef')
            liste = ["facturation", "comptabilité", "documentation", "sacherie", "transfert"
                ,  "archive"]
            lchef = []
            for user1 in all_user:
                if user1.direction in liste:
                    liste.remove(user1.direction)
            message = 'Cet email est déjà utilisé par un autre utilisateur.'
            return render(request, 'templatetra/crer_chef.html',
                          {'util': user, 'message': message,'lstdirection': liste})
        ##############################


        # Mettre à jour les champs selon les données reçues en POST

        ######################
        if form.is_valid() or 1:
            cleaned_data = form.cleaned_data
            instance = Utilisateurs(
                nom=request.POST['nom'],
                prenom=request.POST['prenom'],
                email=request.POST['email'],
                password='chef',
                telephone=request.POST['telephone'],
                direction=request.POST['direction'],
                # direction=user.direction,
                role='chef',

                # form.cleaned_data['direction']
            )
            instance.save()
            # return redirect('/users/login/')
            #return list_chef(request, user.id_utilisateur)
            return  redirect("/doc/listechef/"+ str(request.POST["id_user"]))
        else:
            forms = UtilisateurForm()
            #return Crer_chef_page(request, request.POST["id_user"])
            # return render(request, 'templatetra/crer_agent.html', {'forms': forms})
            return  redirect('/doc/crer_chef_page/' + str(request.POST["id_user"]))



#@csrf_exempt
def update_chef_page(request, id_user, id_chf):
    user = Utilisateurs.objects.get(id_utilisateur=id_user)
    agt = Utilisateurs.objects.get(id_utilisateur=id_chf)
    liste = ["facturation", "comptabilité", "documentation", "sacherie", "transfert"
        , "archive"]
    lchef = []
    all_user = Utilisateurs.objects.filter(role='chef')

    for user1 in all_user:
        if user1.direction in liste:
            liste.remove(user1.direction)
    return render(request, 'templatetra/update_chef.html', {'chf': agt, 'util': user,'liste':liste})


@csrf_exempt
def upadte_chef(request):
        # Récupérer l'utilisateur chef à mettre à jour
        agt = Utilisateurs.objects.get(id_utilisateur=request.POST['id_chf'])

        # Récupérer l'utilisateur qui effectue la mise à jour
        user = Utilisateurs.objects.get(id_utilisateur=request.POST['id_user'])

        # Vérifier si un autre utilisateur utilise déjà l'email fourni
        check_email = Utilisateurs.objects.filter(email=request.POST['email']).exclude(
            id_utilisateur=agt.id_utilisateur).exists()

        # Mettre à jour les champs selon les données reçues en POST
        if request.POST.get('prenom'):
            agt.prenom = request.POST['prenom']
        if request.POST.get('nom'):
            agt.nom = request.POST['nom']
        if request.POST.get('email'):
            if agt.email != request.POST['email']:
                # Vérifier si l'email est déjà utilisé par un autre utilisateur
                if check_email:
                    message = 'Cet email est déjà utilisé par un autre utilisateur.'
                    return render(request, 'templatetra/update_chef.html',
                                  {'chf': agt, 'util': user, 'message': message})
                else:
                    agt.email = request.POST['email']

        if request.POST.get('telephone'):
            agt.telephone = request.POST['telephone']
        if request.POST.get('direction'):
            agt.direction = request.POST['direction']

        # Sauvegarder les modifications dans la base de données
        agt.save()

        # Rediriger l'utilisateur après la mise à jour
        return redirect("/doc/listechef/" + str(user.id_utilisateur))


@csrf_exempt
def desactiver_chef(request, id_user, id_chf):
    user = Utilisateurs.objects.get(id_utilisateur=id_user)
    agt = Utilisateurs.objects.get(id_utilisateur=id_chf)
    agt.etat = 0
    agt.save()
    return redirect("/doc/listechef/" + str(id_user))
    # return list_agent(request,user.id_utilisateur)


@csrf_exempt
def activer_chef(request, id_user, id_chf):
    user = Utilisateurs.objects.get(id_utilisateur=id_user)
    agt = Utilisateurs.objects.get(id_utilisateur=id_chf)
    agt.etat = 1
    agt.save()
    return redirect("/doc/listechef/" + str(id_user))
    # return list_agent(request,user.id_utilisateur)


@csrf_exempt
def reinitiliaser_mdp_chef(request, id_user, id_chf):
    user = Utilisateurs.objects.get(id_utilisateur=id_user)
    agt = Utilisateurs.objects.get(id_utilisateur=id_chf)
    agt.password = '1234'
    agt.save()
    return redirect("/doc/listechef/" + str(id_user))
    # return list_agent(request,user.id_utilisateur)


#########Gestion Demande de suppression

@csrf_exempt
def demandepermission(request,id,id_doc):
    id_user = id

    id_doc = id_doc

    #id_boite = request.POST['id_boite']
    user = Utilisateurs.objects.get(id_utilisateur=id_user)
    user = Utilisateurs.objects.get(id_utilisateur=id_user)
    doc = False
    try:
        doc = RestrictionDocument.objects.get(id_user=id_user, id_doc=id_doc)

    except:
        pass
    if doc:
        doc.dmd = 1
        doc.acces_dir = 1
        doc.save()
        document = Document.objects.get(id_document=doc.id_doc)
        boite = Boite.objects.get(id_boite=document.id_boite)
        # /doc/listedocumentboite/id_boite /id_user
    return redirect("/doc/listedocumentboite/" + str(boite.id_boite) + "/" + str(id_user))
    # return listedocumentboite(request,id_boite,id_user)


@csrf_exempt
def acceptr_permission(request, id, id_user):
    try:
        res = RestrictionDocument.objects.get(id_restric=id)
        res.delete()
    except:
        pass
    # return listpermission(request,id_user)
    return redirect("/doc/liste_permission/" + str(id_user))


@csrf_exempt
def refuser_permission(request, id, id_user):
    try:
        res = RestrictionDocument.objects.get(id_restric=id)
        res.ref = 1
        res.save()
    except:
        pass
    return redirect("/doc/liste_permission/" + str(id_user))
    # return listpermission(request,id_user)


@csrf_exempt
def listpermission(request, id):
    user = Utilisateurs.objects.get(id_utilisateur=id)
    lstuser = Utilisateurs.objects.filter(direction=user.direction)
    listboit = Boite.objects.filter(id_user__in=lstuser)
    listdoc = Document.objects.filter(id_boite__in=listboit)
    Liste_user = Utilisateurs.objects.all()
    #####document no direction
    documents_no_dir = Document.objects.exclude(id_document__in=listdoc.values_list('id_document', flat=True))

    # lisrect=RestrictionDocument.objects.filter(id_doc__in=listdoc,ref=0)
    lisrect = RestrictionDocument.objects.filter(id_chef=id, ref=0, acces_dir=1)
    restricted_ids_doc = set(listdoc.values_list('id_document', flat=True))
    restricted_ids_user = set(Liste_user.values_list('id_utilisateur', flat=True))
    lstdoc_no_dir = set(documents_no_dir.values_list('id_document', flat=True))
    # Ajouter dynamiquement l'attribut 'acces=0' aux documents restreints dans listedoc
    ####doc direction
    us = Utilisateurs.objects.get(id_utilisateur=id)
    lsuserdir = Utilisateurs.objects.filter(direction=us.direction)
    btdir = Boite.objects.filter(id_user__in=lsuserdir)
    docdir = Document.objects.filter(id_boite__in=btdir)
    lstdocdir = set(docdir.values_list('id_document', flat=True))

    for doc in lisrect:

        user = Utilisateurs.objects.get(id_utilisateur=id)
        if doc.service == user.direction:
            doc.mdir = 1
        else:
            doc.mdir = 0

        if doc.id_doc in restricted_ids_doc:
            doc.dir = 1
            docu = Document.objects.get(id_document=doc.id_doc)
            # doc.document=docu.chemin_acces
            if doc.id_user in restricted_ids_user:
                useru = Utilisateurs.objects.get(id_utilisateur=doc.id_user)
                doc.document = docu.chemin_acces
                doc.numero = docu.numero_docuemnt
                doc.user = useru.prenom + ' ' + useru.nom
                doc.direction = user.direction
        if doc.id_doc in lstdoc_no_dir:
            doc.dir = 0
            docu = Document.objects.get(id_document=doc.id_doc)
            # doc.document=docu.chemin_acces

            if doc.id_user in restricted_ids_user:
                useru = Utilisateurs.objects.get(id_utilisateur=doc.id_user)
                doc.document = docu.chemin_acces
                doc.numero = docu.numero_docuemnt
                doc.user = useru.prenom + ' ' + useru.nom
                doc.direction = user.direction

    return render(request, 'templatetra/liste_permission.html', {'lstres': lisrect, 'util': user})


################Demande Tout

@csrf_exempt
def demande_acces_document_tout(request, id, id_doc):
    user = Utilisateurs.objects.get(id_utilisateur=id)
    doc = Document.objects.get(id_document=id_doc)
    return render(request, 'templatetra/ajouter_demande_tout.html', {'util': user, 'doc': doc})


@csrf_exempt
def enregistrer_demande_doc_tout(request):
    dmd = Demande(
        type='document',
        commentaire=request.POST['commentaire'],
        date_dmd=datetime.now(),
        id_demandeur=request.POST['id_user'],
        id_docuement=request.POST['id_doc']

    )
    dmd.save()
    return redirect("/doc/tot_document/" + str(request.POST['id_user']))

    # return tout_doc(request,)

@csrf_exempt
def demandepermission_tout(request, id, id_doc):
    user = Utilisateurs.objects.get(id_utilisateur=id)
    try:
        doc = RestrictionDocument.objects.get(id_user=id, id_doc=id_doc)
        doc.acces = 0
        doc.etat = 1
        doc.dmd = 1
        doc.ref = 0
        doc.acces_dir = 1
        doc.save()
        document = Document.objects.get(id_document=doc.id_doc)
        boite = Boite.objects.get(id_boite=document.id_boite)
    except:
        pass

    return tout_doc(request, id)
    # listedocumentboite(request,id_boite,user.id_utilisateur)


@csrf_exempt
def voire_document_demande(request, id_user, id_doc):
    doc = Document.objects.get(id_document=id_doc)
    user = Utilisateurs.objects.get(id_utilisateur=id_user)
    return render(request, 'templatetra/voir_demande_document.html',
                  {'doc': doc, 'util': user})


@csrf_exempt
def mes_demandes(request, id):
    user = Utilisateurs.objects.get(id_utilisateur=id)
    res = RestrictionDocument.objects.filter(id_user=id)

    return render(request, 'templatetra/mes_demandes.html', {'lstres': res, 'util': user})


########GESTION DES DEMNADES DE CONSULTATIONS
@csrf_exempt
def mes_consultations(request, id):
    dmd = Demande.objects.filter(id_demandeur=id)
    user = Utilisateurs.objects.get(id_utilisateur=id)
    return render(request, 'templatetra/mes_demandes_consultations.html', {'cons': dmd, 'util': user})


######################GESTION DES DEMANDES DE PERMISSION TOUT
@csrf_exempt
def retriction_page_tout(request, id, id_doc):
    user = Utilisateurs.objects.get(id_utilisateur=id)
    agt = Utilisateurs.objects.filter(direction=user.direction, role='agent')
    res_doc = RestrictionDocument.objects.filter(id_doc=id_doc)

    res_doc_acces = RestrictionDocument.objects.filter(id_doc=id_doc, acces_dir=3)
    rgbt_ids = set(res_doc_acces.values_list('id_user', flat=True))
    agt_acces = Utilisateurs.objects.filter(id_utilisateur__in=rgbt_ids)

    agt = Utilisateurs.objects.filter(direction=user.direction).exclude(id_utilisateur=user.id_utilisateur).union(
        agt_acces)

    # agt = Utilisateurs.objects.filter(direction=user.direction).exclude(id_utilisateur=user.id_utilisateur)
    for agent_id in res_doc:
        # agt.exclude(id_utilisateur=agent_id.id_user)
        # agt.filter(id_utilisateur=agent_id.id_user).delete()
        agt = [agent for agent in agt if agent.id_utilisateur != agent_id.id_user]
    doc = Document.objects.get(id_document=id_doc)

    doc = Document.objects.get(id_document=id_doc)
    agt_dir = Utilisateurs.objects.filter(id_utilisateur__in=rgbt_ids)

    return render(request,  'templatetra/restriction_tout.html', {'util': user, 'doc': doc, 'agt': agt, 'agt_dir': agt_dir})

    #return render(request, 'templatetra/restriction_tout.html', {'util': user, 'doc': doc, 'agt': agt,'agt_dir':agt_dir})


@csrf_exempt
def enregistrer_restriction_tout(request):
    selected_agents = request.POST.getlist('agents')  # Récupère toutes les valeurs sélectionnées
    selected_agents = request.POST.getlist('agt')  # Récupère toutes les valeurs sélectionnées
    util = Utilisateurs.objects.get(id_utilisateur=request.POST['id_user'])

    for agent_id in selected_agents:

        docu = Document.objects.get(id_document=request.POST['id_doc'])
        boite = Boite.objects.get(id_boite=docu.id_boite)
        user = Utilisateurs.objects.get(id_utilisateur=boite.id_user)
        user_crt = Utilisateurs.objects.get(id_utilisateur=agent_id)
        if  user_crt.direction == util.direction :
            if not RestrictionDocument.objects.filter(id_doc=request.POST['id_doc'], id_user=agent_id).exists():
                res = RestrictionDocument(
                    id_user=agent_id,  # Utilise agent_id directement
                    id_doc=request.POST['id_doc'],
                    numero_docuent=docu.numero_docuemnt,
                    service=user.direction,
                    date_dmd=datetime.now(),
                    acces=0,
                    etat=1,
                    id_chef=user.id_utilisateur
                )
                res.save()
        else :
            util = Utilisateurs.objects.get(id_utilisateur=request.POST['id_user'])
            RestrictionDocument.objects.filter(id_doc=request.POST['id_doc'], id_user=agent_id).delete()

    doc = Document.objects.get(id_document=request.POST['id_doc'])
    return redirect("/doc/tot_document/" + str(request.POST['id_user']))
    # return tout_doc(request,user.id_utilisateur)


@csrf_exempt
def demandepermission_tout(request, id, id_doc):
    user = Utilisateurs.objects.get(id_utilisateur=id)
    try:
        doc = RestrictionDocument.objects.get(id_user=id, id_doc=id_doc)
        doc.dmd = 1
        doc.acces_dir = 1
        doc.save()
    except:
        pass
    # tot_document / < int: id >
    return redirect("/doc/tot_document/" + str(id))


#########################Voir details Consultation
@csrf_exempt
def voir_detail_boite_consultation(request, id, id_user):
    boite = False
    user = False
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
        return mes_consultations(request, id_user)


@csrf_exempt
def voire_document_consul(request, id, id_user):
    doc = Document.objects.get(id_document=id)
    user = Utilisateurs.objects.get(id_utilisateur=id_user)
    return render(request, 'templatetra/voir_document_consultation.html',
                  {'doc': doc, 'util': user})


@csrf_exempt
def voir_detail_document_consultation(request, id, id_user):
    boite = False
    doc = False
    user = False
    try:
        dmd = Demande.objects.get(id_dmd=id)
        doc = Document.objects.get(id_document=dmd.id_docuement)
        boite = Boite.objects.get(id_boite=doc.id_boite)

    except:
        pass
    user = Utilisateurs.objects.get(id_utilisateur=id_user)
    if doc:
        # return render(request, 'templatetra/voir_document_consultation.html',{'boite': boite,'doc': doc, 'user': user, 'util': user})
        return render(request, 'templatetra/detail_document_consultation.html',
                      {'boite': boite, 'doc': doc, 'user': user, 'util': user})
    else:
        return mes_consultations(request, id_user)


# def repondre_demande(request,id_user,id_obt):

#######################################Peermisoon non direction
@csrf_exempt
def demandepermission_tout_direction(request, id, id_doc):
    docu = Document.objects.get(id_document=id_doc)
    user = Utilisateurs.objects.get(id_utilisateur=id)
    if RestrictionDocument.objects.filter(id_user=user.id_utilisateur, id_doc=id_doc).exists():
        return tout_doc(request, user.id_utilisateur)
    res = RestrictionDocument(
        id_user=id,  # Utilise agent_id directement
        id_doc=id_doc,
        numero_docuent=docu.numero_docuemnt,
        service=user.direction,
        date_dmd=datetime.now(),
        acces=0,
        etat=0,

    )
    res.save()
    # doc=Document.objects.get(id_document=request.POST['id_doc'])
    return tout_doc(request, user.id_utilisateur)


#################Gestion Permission Non direction
@csrf_exempt
def demandepermission_tout_non_dir(request, id, id_doc):
    docu = Document.objects.get(id_document=id_doc)
    docbt = Document.objects.get(id_document=id_doc)
    bt = Boite.objects.get(id_boite=docbt.id_boite)
    userbt = Boite.objects.get(id_boite=bt.id_boite)
    userls = Utilisateurs.objects.get(id_utilisateur=userbt.id_user)
    chef = Utilisateurs.objects.get(direction=userls.direction, role='chef')
    user = Utilisateurs.objects.get(id_utilisateur=id)
    if RestrictionDocument.objects.filter(id_user=user.id_utilisateur, id_doc=id_doc).exists():
        return tout_doc(request, user.id_utilisateur)
    res = RestrictionDocument(
        id_user=id,  # Utilise agent_id directement
        id_doc=id_doc,
        numero_docuent=docu.numero_docuemnt,
        service=user.direction,
        date_dmd=datetime.now(),
        acces=0,
        etat=1,
        dmd=1,
        ref=0,
        acces_dir=1,
        id_chef=chef.id_utilisateur
    )
    res.save()
    # user.id_utilisateur
    return redirect("/doc/tot_document/" + str(id))
    # return tout_doc(request,id)


@csrf_exempt
def refuser_permission_non_dir(request, id, id_user):
    try:
        res = RestrictionDocument.objects.get(id_restric=id)
        res.acces_dir = 2
        res.save()
    except:
        pass
    # return listpermission(request,id_user)
    return redirect("/doc/liste_permission/" + str(id_user))


@csrf_exempt
def accepter_permission_non_ditr(request, id, id_user):
    try:
        res = RestrictionDocument.objects.get(id_restric=id)
        res.acces_dir = 3
        res.save()
    except:
        pass
    # return listpermission(request,id_user)
    return redirect("/doc/liste_permission/" + str(id_user))


################################Gestion Management
@csrf_exempt
def listecartable(request, id):
    lisboite = []
    # a = request.session.get('user_id')
    user = Utilisateurs.objects.get(id_utilisateur=id)
    direction = user.direction
    listuser = Utilisateurs.objects.filter(direction=direction)
    lst_dt_dmd = Demande.objects.filter(id_demandeur=id)
    restricted_doc_ids = set(lst_dt_dmd.values_list('id_boite', flat=True))
    try:
        lisboite = Boite.objects.filter(id_user=id)
        for bt in lisboite:
            if bt.id_boite in restricted_doc_ids:
                bt.cons = 1
            else:
                bt.cons = 0
    except:
        pass
    return render(request, 'templatetra/list_cartable.html', {'boite': lisboite, 'user': user, 'util': user})


@csrf_exempt
def ajoutercartable_page(request, id):
    forms = BoiteForm()
    # id=request.session.get('user_id')
    user = Utilisateurs.objects.get(id_utilisateur=id)
    # return render(request, 'docs/ajouterboite.html', {'form': forms, 'user': user, 'util': user})
    return render(request, 'templatetra/ajout-cartable.html', {'form': forms, 'user': user, 'util': user})


@csrf_exempt
def enregistrer_cartable(request):
    message='La mention saisie existe déja'
    if request.method == 'POST':
        form = BoiteForm(request.POST)
        id_user = request.session.get('user_id')
        if not Boite.objects.filter(mention="CAT" + request.POST['mention']).exists():
            # return ajoutercartable_page(request, request.POST['id_user'])
            # cleaned_data = form.cleaned_data
            # else :
            instance = Boite(
                mention='CAT' + request.POST['mention'],
                date_creation=datetime.now(),
                id_user=request.POST['id_user']
            )
            instance.save()
            return redirect("/doc/listecartable/" + str(request.POST['id_user']))
        else:
            user = Utilisateurs.objects.get(id_utilisateur=request.POST['id_user'])
            # return render(request, 'docs/ajouterboite.html', {'form': forms, 'user': user, 'util': user})
            return render(request, 'templatetra/ajout-cartable.html', { 'user': user, 'util': user,'message': message})

            #return redirect("/doc/ajoutercartable_page/" + str(request.POST['id_user']))

    else:
        user = Utilisateurs.objects.get(id_utilisateur=request.POST['id_user'])
        # return render(request, 'docs/ajouterboite.html', {'form': forms, 'user': user, 'util': user})
        return render(request, 'templatetra/ajout-cartable.html', {'user': user, 'util': user,'message': message})

        #return redirect("/doc/ajoutercartable_page/" + str(request.POST['id_user']))


@csrf_exempt
def listedocument_cartable(request, id, id_user):
    listedoc = []
    boite = False
    listres = RestrictionDocument.objects.filter(id_user=id_user)
    user = False

    try:
        listedoc = Document.objects.filter(id_boite=id)

        boite = Boite.objects.get(id_boite=id)

    except:
        pass
    ###liste des documents restraintre
    restricted_doc_ids = set(listres.values_list('id_doc', flat=True))
    lst_doc_dmd = Demande.objects.filter(id_demandeur=id_user)
    restricted_doc_dmd_ids = set(lst_doc_dmd.values_list('id_docuement', flat=True))

    # Ajouter dynamiquement l'attribut 'acces=0' aux documents restreints dans listedoc
    for doc in listedoc:
        if doc.id_document in restricted_doc_dmd_ids:
            doc.cons = 0
        else:
            doc.cons = 1

        if doc.id_document in restricted_doc_ids:
            docres = RestrictionDocument.objects.get(id_user=id_user, id_doc=doc.id_document)
            doc.ref = docres.ref
            doc.dmd = docres.dmd
            doc.acces = 0
            doc.etat = 1
        else:
            doc.acces = 1

    user = Utilisateurs.objects.get(id_utilisateur=id_user)
    return render(request, 'templatetra/list_document_cartble.html',
                  {'doc': listedoc, 'user': user, 'util': user, 'boite': boite})


@csrf_exempt
def ajouterdocumentcartable_page(request, id):
    forms = DocumentForm()
    boite = Boite.objects.get(id_boite=id)
    user = Utilisateurs.objects.get(id_utilisateur=boite.id_user)
    # return render(request, 'docs/ajouerterdossier.html', {'form': forms, 'user': user, 'util': user, 'boite': boite})
    return render(request, 'templatetra/ajoutdocumentcartable.html',
                  {'form': forms, 'user': user, 'util': user, 'boite': boite})


@csrf_exempt
def ajouterdocumentcartbale(request):
    if request.method == 'POST':
        form = BoiteForm(request.POST)
        user = False
        boite = False
        try:
            user = Utilisateurs.objects.get(id_utilisateur=request.POST['id_user'])
            boite = Boite.objects.get(id_boite=request.POST['id_boite'])
        except:
            pass
        fichier = request.FILES['file']
        handle_uploaded_file(fichier)
        current_timestamp = int(datetime.timestamp(datetime.now()))
        if form.is_valid() or 1:
            # derniere_per = Permission.objects.latest(' id_permission')
            ####Ajoter Document
            if Document.objects.filter(numero_docuemnt=str('CAT') + request.POST['numero']).exists() or Document.objects.filter(bl=request.POST['bl']).exists():
                message = ''
                messagebl = ''
                if Document.objects.filter(numero_docuemnt=str('CAT') + request.POST['numero']).exists():
                    message = 'L\'identifiant mentionné existe deja'
                if Document.objects.filter(bl=request.POST['bl']).exists():
                    messagebl= 'Le BL mentionné exite déja'
                return render(request, 'templatetra/ajoutdocumentcartable.html',
                              { 'user': user, 'util': user, 'boite': boite,'message': message, 'messagebl': messagebl})
                #return ajouterdossier_page(request, request.POST['id_boite'])
            instance = Document(numero_docuemnt='CAT' + request.POST['numero'],
                                date_creation=datetime.now(),
                                chemin_acces=str(current_timestamp) + fichier.name,
                                eta=request.POST['eta'],
                                bl=request.POST['bl'],
                                client=request.POST['client'],
                                nom_navire=request.POST['navire'],
                                numero_voyage=request.POST['voyage'],
                                id_boite=request.POST['id_boite'],
                                id_per=2
                                )
            instance.save()

            return redirect(
                "/doc/liste_document_catble/" + str(request.POST['id_boite']) + "/" + str(request.POST['id_user']))
    else:
        forms = DocumentForm()
        boite = Boite.objects.get(id_boite=request.POST['boite'])
        user = Utilisateurs.objects.get(id_user=boite.id_user)
        return redirect("/doc/ajouterdocument_cartable/" + str(request.POST['boite']))
        # return render(request, 'docs/ajou',
        #            {'forms': forms, 'user': user, 'util': user, 'boiie': boite})


@csrf_exempt
def handle_uploaded_file(f):
    current_timestamp = int(datetime.timestamp(datetime.now()))
    with open('static/archives/' + str(current_timestamp) + f.name, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)


@csrf_exempt
def voire_document_cartable(request, id, id_user):
    doc = Document.objects.get(id_document=id)
    user = Utilisateurs.objects.get(id_utilisateur=id_user)
    return render(request, 'templatetra/voir_document_cartable.html',
                  {'doc': doc, 'util': user})


@csrf_exempt
def classerCartable_page(request, id, id_user):
    boite = Boite.objects.get(id_boite=id)

    user = Utilisateurs.objects.get(id_utilisateur=id_user)
    return render(request, 'templatetra/classer_cartable.html',
                  {'user': user, 'util': user, 'boite': boite})


@csrf_exempt
def classercartable(request):
    if request.method == 'POST':
        id = request.POST['id_user']
        id_boite = request.POST['id_boite']
        id_user = request.POST['id_user']

        if   1:
            boit = Boite.objects.get(id_boite=id_boite)
            # boit.numero_rang = request.POST['numerorang']
            # boit.harmoire = request.POST['armoire']
            # boit.numero_comp = request.POST['com']
            boit.commentaire = request.POST['commentaire']
            # boit.etat=1
            boit.save()
            return redirect("/doc/listecartable/" + str(request.POST['id_user']))

        # return listecartable(request,request.POST['id_user'])

        else:
            return redirect("/doc/classerCartable/" + str(id_boite) + "" + str(id_user))


@csrf_exempt
def clotureCartable(request, id):
    boite = False
    user = False
    try:
        boite = Boite.objects.get(id_boite=id)
        boite.etat = 0
        boite.save()

    except:
        pass
    user = Utilisateurs.objects.get(id_utilisateur=boite.id_user)
    if boite:
        return redirect("/doc/listecartable/" + str(user.id_utilisateur))
        # return listeboitedirection(request, user.id_utilisateur)

    # return listedocumentboite(request, id)
    return redirect("liste_document_catble/" + str(id) + "/" + str(user.id_utilisateur))


@csrf_exempt
def retriction_manage_page(request, id, id_doc):
    user = Utilisateurs.objects.get(id_utilisateur=id)
    user = Utilisateurs.objects.get(id_utilisateur=id)
    # agt = Utilisateurs.objects.filter(direction=user.direction).exclude(id_utilisateur=user.id_utilisateur)
    # doc=Document.objects.get(id_document=id_doc)
    res_doc = RestrictionDocument.objects.filter(id_doc=id_doc)
    agt = Utilisateurs.objects.filter(direction=user.direction).exclude(id_utilisateur=user.id_utilisateur)
    for agent_id in res_doc:
        # agt.exclude(id_utilisateur=agent_id.id_user)
        # agt.filter(id_utilisateur=agent_id.id_user).delete()
        agt = [agent for agent in agt if agent.id_utilisateur != agent_id.id_user]
    doc = Document.objects.get(id_document=id_doc)
    return render(request, 'templatetra/restreindremanagement.html', {'util': user, 'doc': doc, 'agt': agt})


@csrf_exempt
def enregistrer_restriction_manage(request):
    selected_agents = request.POST.getlist('agents')  # Récupère toutes les valeurs sélectionnées
    selected_agents = request.POST.getlist('agt')  # Récupère toutes les valeurs sélectionnées
    for agent_id in selected_agents:
        docu = Document.objects.get(id_document=request.POST['id_doc'])
        boite = Boite.objects.get(id_boite=docu.id_boite)
        user = Utilisateurs.objects.get(id_utilisateur=boite.id_user)
        if not RestrictionDocument.objects.filter(id_doc=request.POST['id_doc'], id_user=agent_id).exists():
            res = RestrictionDocument(
                id_user=agent_id,  # Utilise agent_id directement
                id_doc=request.POST['id_doc'],
                numero_docuent=docu.numero_docuemnt,
                service=user.direction,
                date_dmd=datetime.now(),
                acces=0,
                etat=1,
                id_chef=request.POST['id_user']
            )
            res.save()
    doc = Document.objects.get(id_document=request.POST['id_doc'])
    return redirect("/doc/liste_document_catble/" + str(doc.id_boite) + "/" + str(request.POST['id_user']))
    # <int:id>/<int:id_user>'"
    # return listedocumentboite(request,doc.id_boite,request.POST['id_user'])


@require_POST
@csrf_exempt
def demandepermission_manage(request):
    id_user = request.POST['id_user']

    id_doc = request.POST['id_doc']

    id_boite = request.POST['id_boite']
    user = Utilisateurs.objects.get(id_utilisateur=id_user)
    user = Utilisateurs.objects.get(id_utilisateur=id_user)
    doc = False
    try:
        doc = RestrictionDocument.objects.get(id_user=id_user, id_doc=id_doc)

    except:
        pass
    if doc:
        doc.dmd = 1
        doc.acces_dir = 1
        doc.save()
        document = Document.objects.get(id_document=doc.id_doc)
        boite = Boilistedocument_cartablete.objects.get(id_boite=document.id_boite)
        # /doc/listedocumentboite/id_boite /id_user
    return redirect("/doc/liste_document_catble/" + id_boite + "/" + id_user)


###############################Gestion tout document Management
@csrf_exempt
def tout_doc_management(request, id):
    user = Utilisateurs.objects.get(id_utilisateur=id)
    bt_user = Boite.objects.filter(id_user=id)
    doc_bt = Document.objects.filter(id_boite__in=bt_user)
    doc_bt_ids = set(doc_bt.values_list('id_document', flat=True))
    lst_doc = Document.objects.filter(numero_docuemnt__startswith='CAT')
    lst_doc_ids = set(lst_doc.values_list('id_document', flat=True))
    ls_doc_res = RestrictionDocument.objects.filter(id_doc__in=lst_doc)
    ls_doc_res_ids = set(ls_doc_res.values_list('id_doc', flat=True))
    ######boite  ranger
    lisboite_rg = Boite.objects.exclude(numero_rang__startswith='Auc')
    boite_range = set(lisboite_rg.values_list('id_boite', flat=True))
    ######doc occupe
    lisboite_occupe = Demande.objects.filter(id_demandeur=id, etat__in=[0, 1], date_retour__isnull=True)
    doc_occupe = set(lisboite_occupe.values_list('id_docuement', flat=True))
    #####Restriction
    lst_res = RestrictionDocument.objects.filter(acces_dir=3)
    lst_res_ids = set(lst_res.values_list('id_doc', flat=True))
    for doc in lst_doc:
        if doc.id_document in lst_res_ids:
            doc.res = 1
        else:
            doc.res = 0
        if doc.id_document in doc_occupe:
            doc.occ = 1
        else:
            doc.occ = 0

        if doc.id_boite in boite_range:
            doc.rg = 1
        else:
            doc.rg = 0
        # doc.id=doc.id_document
        if doc.id_document in doc_bt_ids:
            doc.app = 1
        else:
            doc.app = 0
        if doc.id_document in ls_doc_res_ids:
            try:
                docres = RestrictionDocument.objects.get(id_doc=doc.id_document, id_user=id)
                doc.ref = docres.ref
                doc.dmd = docres.dmd
                docacces = docres.acces
                doc.acces_dir = docres.acces_dir
                doc.per = 0
            except:
                pass
                doc.per = 1
        else:
            doc.acces = 1
            doc.per = 1
    return render(request, 'templatetra/tout_document_manage.html', {'util': user, 'doc': lst_doc})


@csrf_exempt
def demandepermission_managment(request, id, id_doc):
    docu = Document.objects.get(id_document=id_doc)
    bt = Boite.objects.get(id_boite=docu.id_boite)
    chef = Utilisateurs.objects.get(id_utilisateur=bt.id_user)
    user = Utilisateurs.objects.get(id_utilisateur=id)
    if RestrictionDocument.objects.filter(id_user=user.id_utilisateur, id_doc=id_doc).exists():
        return tout_doc(request, user.id_utilisateur)
    res = RestrictionDocument(
        id_user=id,  # Utilise agent_id directement
        id_doc=id_doc,
        numero_docuent=docu.numero_docuemnt,
        service=user.direction,
        date_dmd=datetime.now(),
        acces=0,
        etat=1,
        dmd=1,
        ref=0,
        acces_dir=1,
        id_chef=chef.id_utilisateur
    )
    res.save()
    # user.id_utilisateur
    return redirect("/doc/tout_document_manag/" + str(id))


@csrf_exempt
def voir_tout_document_manag(request, id, id_user):
    doc = Document.objects.get(id_document=id)
    user = Utilisateurs.objects.get(id_utilisateur=id_user)
    return render(request, 'templatetra/voir_tout_document_manage.html',
                  {'doc': doc, 'util': user})


@csrf_exempt
def listpermission_manage(request, id):
    lisrect = RestrictionDocument.objects.filter(id_chef=id, ref=0, acces_dir=1)
    user = Utilisateurs.objects.get(id_utilisateur=id)

    for doc in lisrect:
        useru = Utilisateurs.objects.get(id_utilisateur=doc.id_user)
        docu = Document.objects.get(id_document=doc.id_doc)  #
        doc.document = docu.chemin_acces
        doc.numero = docu.numero_docuemnt
        doc.user = useru.prenom + ' ' + useru.nom
    return render(request, 'templatetra/liste_permission_manage.html', {'lstres': lisrect, 'util': user})


@csrf_exempt
def refuser_permission_manage(request, id, id_user):
    try:
        res = RestrictionDocument.objects.get(id_restric=id)
        res.acces_dir = 2
        res.save()
    except:
        pass
    # return listpermission(request,id_user)
    return redirect("/doc/liste_permission_manage/" + str(id_user))


@csrf_exempt
def accepter_permission_management(request, id, id_user):
    try:
        res = RestrictionDocument.objects.get(id_restric=id)
        res.acces_dir = 3
        res.save()
    except:
        pass
    # return listpermission(request,id_user)
    return redirect("/doc/liste_permission_manage/" + str(id_user))


#########################################Grestion restriction tout

@csrf_exempt
def retriction_manage_page_tout(request, id, id_doc):
    user = Utilisateurs.objects.get(id_utilisateur=id)
    user = Utilisateurs.objects.get(id_utilisateur=id)
    res_doc = RestrictionDocument.objects.filter(id_doc=id_doc, acces_dir=3)
    res_doc_ids = res_doc.values_list('id_user', flat=True)
    agt = Utilisateurs.objects.filter(id_utilisateur__in=res_doc_ids)
    # agt = Utilisateurs.objects.filter(direction=user.direction).exclude(id_utilisateur=user.id_utilisateur)

    # for agent_id in res_doc:
    # agt.exclude(id_utilisateur=agent_id.id_user)
    # agt.filter(id_utilisateur=agent_id.id_user).delete()
    # agt = [agent for agent in agt if agent.id_utilisateur != agent_id.id_user]
    doc = Document.objects.get(id_document=id_doc)
    return render(request, 'templatetra/restreindremanagement_tout.html', {'util': user, 'doc': doc, 'agt': agt})


@csrf_exempt
def enregistrer_restriction_manage_tout(request):
    selected_agents = request.POST.getlist('agents')  # Récupère toutes les valeurs sélectionnées
    selected_agents = request.POST.getlist('agt')  # Récupère toutes les valeurs sélectionnées
    for agent_id in selected_agents:
        docu = Document.objects.get(id_document=request.POST['id_doc'])
        boite = Boite.objects.get(id_boite=docu.id_boite)
        user = Utilisateurs.objects.get(id_utilisateur=boite.id_user)
        if not RestrictionDocument.objects.filter(id_doc=request.POST['id_doc'], id_user=agent_id).exists():
            res = RestrictionDocument(
                id_user=agent_id,  # Utilise agent_id directement
                id_doc=request.POST['id_doc'],
                numero_docuent=docu.numero_docuemnt,
                service=user.direction,
                date_dmd=datetime.now(),
                acces=0,
                etat=1,
                id_chef=request.POST['id_user']
            )
            # res.save()
        res = RestrictionDocument.objects.get(id_user=agent_id, id_doc=request.POST['id_doc'])
        res.delete()
    # doc=Document.objects.get(id_document=request.POST['id_doc'])
    return redirect("/doc/tout_doc_manage/" + str(request.POST['id_user']))
    # <int:id>/<int:id_user>'"
    # return listedocumentboite(request,doc.id_boite,request.POST['id_user'])


@csrf_exempt
def demandepermission_manage_tout(request, id_user, id_doc):
    # id_user = request.POST['id_user']

    # id_doc = request.POST['id_doc']
    docu = Document.objects.get(id_document=id_doc)
    bt = Boite.objects.get(id_boite=docu.id_boite)

    # id_boite = request.POST['id_boite']
    user = Utilisateurs.objects.get(id_utilisateur=id_user)
    user = Utilisateurs.objects.get(id_utilisateur=id_user)
    if RestrictionDocument.objects.filter(id_user=user.id_utilisateur, id_doc=id_doc).exists():
        return redirect("/doc/tout_doc_manage/" + str(id_user))
    res = RestrictionDocument(
        id_user=id_user,  # Utilise agent_id directement
        id_doc=id_doc,
        numero_docuent=docu.numero_docuemnt,
        service=user.direction,
        date_dmd=datetime.now(),
        acces=0,
        etat=1,
        dmd=1,
        ref=0,
        acces_dir=1,
        id_chef=bt.id_user
    )
    res.save()
    return redirect("/doc/tout_doc_manage/" + str(id_user))


@csrf_exempt
def voire_document_demande_manage(request, id_user, id_doc):
    doc = Document.objects.get(id_document=id_doc)
    user = Utilisateurs.objects.get(id_utilisateur=id_user)
    return render(request, 'templatetra/voir_docu,ent_demande_manage.html',
                  {'doc': doc, 'util': user})


@csrf_exempt
def voir_tout_document_manage(request, id, id_user):
    doc = Document.objects.get(id_document=id)
    user = Utilisateurs.objects.get(id_utilisateur=id_user)
    return render(request, 'templatetra/voir_tout_document_manage.html',
                  {'doc': doc, 'util': user})


#######################Gestion document globale
@csrf_exempt
def global_doc(request, id):
    # listedoc=Document.objects.all()
    listedoc = Document.objects.exclude(numero_docuemnt__startswith='CAT')
    ######boite  ranger
    lisboite_rg = Boite.objects.exclude(numero_rang__startswith='Auc')
    boite_range = set(lisboite_rg.values_list('id_boite', flat=True))
    ######doc occupe
    lisboite_occupe = Demande.objects.filter(id_demandeur=id, etat__in=[0, 1], date_retour__isnull=True)
    doc_occupe = set(lisboite_occupe.values_list('id_docuement', flat=True))
    # Ajouter dynamiquement l'attribut 'acces=0' aux documents restreints dans listedoc
    for doc in listedoc:
        if doc.id_document in doc_occupe:
            doc.occ = 1
        else:
            doc.occ = 0

        if doc.id_boite in boite_range:
            doc.rg = 1
        else:
            doc.rg = 0

    user = Utilisateurs.objects.get(id_utilisateur=id)

    return render(request, 'templatetra/document_global_manage.html', {'util': user, 'doc': listedoc})


@csrf_exempt
def voir_document_globale(request, id, id_user):
    doc = Document.objects.get(id_document=id)
    user = Utilisateurs.objects.get(id_utilisateur=id_user)
    return render(request, 'templatetra/voir_document_global.html',
                  {'doc': doc, 'util': user})


##########################Gestrion Consultataion

@csrf_exempt
def demande_acces_document_globale(request, id, id_doc):
    user = Utilisateurs.objects.get(id_utilisateur=id)
    doc = Document.objects.get(id_document=id_doc)
    return render(request, 'templatetra/ajouter_demande_globale.html', {'util': user, 'doc': doc})


@csrf_exempt
def enregistrer_demande_doc_globale(request):
    dmd = Demande(
        type='document',
        commentaire=request.POST['commentaire'],
        date_dmd=datetime.now(),
        id_demandeur=request.POST['id_user'],
        id_docuement=request.POST['id_doc']

    )
    dmd.save()
    return redirect("/doc/glo_document/" + str(request.POST['id_user']))

    # return tout_doc(request,request.POST['id_user'])


###################Gestion
from django.http import JsonResponse
# from .models import YourModel  # Remplacez par le modèle que vous utilisez

from django.http import JsonResponse
from .models import Document


def fetch_data(request, id):
    id_user = request.GET.get('id_user')
    if id_user:
        id_user = int(id_user)
        # Get user information
    # useru = Utilisateurs.objects.get(id_utilisateur=17)
    bt_user = Boite.objects.filter(id_user=id_user)
    bt_ids = set(bt_user.values_list('id_boite', flat=True))
    doc_bt = Document.objects.filter(id_boite__in=bt_ids)
    doc_bt_ids = set(doc_bt.values_list('id_document', flat=True))

    # Update document restrictions before creating data
    lst_res = RestrictionDocument.objects.filter(id_user=id_user)
    lst_res_ids = set(lst_res.values_list('id_doc', flat=True))

    ######restriction
    lst_res_acces = RestrictionDocument.objects.filter(acces_dir=3)
    lst_res_ids_acces = set(lst_res_acces.values_list('id_doc', flat=True))

    # appartien et acces
    doc_per = RestrictionDocument.objects.filter(id_user=id_user, acces_dir__in=[1, 3])
    boite = Boite.objects.exclude(id_user=id_user)

    doc_per_ids = set(lst_res.values_list('id_doc', flat=True))

    lst_doc = Document.objects.filter(numero_docuemnt__startswith='CAT')

    data = []

    for document in lst_doc:
        # Check for restricted access based on lst_res_ids
        document.res = 1 if document.id_document in lst_res_ids_acces else 0
        document.app = 1 if document.id_document in doc_bt_ids else 0
        # document.per = 1 if document.id_document in doc_per_ids else 0

        if document.id_document in lst_res_ids:

            try:
                # Try to retrieve restriction details for the user
                docres = RestrictionDocument.objects.get(id_doc=document.id_document, id_user=id_user)
                document.acces_dirr = docres.acces_dir
            except RestrictionDocument.DoesNotExist:

                document.acces_dirr = 11

        else:
            document.acces_dirr = 8

        data.append({
            'id': document.id_document,
            'bl': document.bl,
            'date_creation':  format(document.date_creation, 'd F Y'),
            'client': document.client,
            #'eta': document.eta,
            'eta': format(document.eta, 'd F Y'),
            'nom_navire': document.nom_navire,
            'numero_voyage': document.numero_voyage,
            'res': document.res,
            'appp': document.app,
            'acces_dirr': document.acces_dirr,  # Assuming all documents have acces_dir set to 3
            # Assuming all documents have per set to 1 (modify if needed)
            'numero_document': document.numero_docuemnt,
            # ... other fields
        })

    return JsonResponse({'data': data})


def fetch_permision_data(request, id):
    id_user = request.GET.get('id_user')
    if id_user:
        id_user = int(id_user)
    lisrect = RestrictionDocument.objects.filter(id_chef=id_user, ref=0, acces_dir=1)
    user = Utilisateurs.objects.get(id_utilisateur=id_user)
    data = []
    for doc in lisrect:
        useru = Utilisateurs.objects.get(id_utilisateur=doc.id_user)
        docu = Document.objects.get(id_document=doc.id_doc)  #
        doc.document = docu.chemin_acces
        doc.numero = docu.numero_docuemnt
        doc.user = useru.prenom + ' ' + useru.prenom
        doc.id_doc = docu.id_document
        data.append({
            'id': doc.id_restric,
            'numero_document': doc.numero,
            'user': doc.user,
            'id_doc': doc.id_doc

            # ... other fields
        })

    return JsonResponse({'data': data})


def fetch_document_boite(request, id):
    id_user = request.GET.get('id_user')
    bte = request.GET.get('bte')
    if id_user:
        id_user = int(id_user)
        # Get user information
    if bte:
        bte = int(bte)
        # Get user information
    listedoc = []
    boite = False
    listres = RestrictionDocument.objects.filter(id_user=id_user)
    lst_bt_dmd = Demande.objects.filter(id_boite=bte)
    doc_bt_dmd = Document.objects.filter(id_boite__in=lst_bt_dmd)
    #####Document boite en cours
    doc_bt = Document.objects.filter(id_boite=bte)
    bt_dmd = Document.objects.filter(id_boite=bte)
    doc_bt_dmd_crs = Document.objects.filter(id_boite__in=bt_dmd)
    user = False
    lisboite = Boite.objects.exclude(numero_rang__startswith='Auc')

    try:
        listedoc = Document.objects.filter(id_boite=bte)

        boite = Boite.objects.get(id_boite=bte)

    except:
        pass
    ###liste des documents restraintre
    restricted_doc_ids = set(listres.values_list('id_doc', flat=True))
    restricted_doc_bt__ids = set(doc_bt_dmd.values_list('id_document', flat=True))
    restricted_bt_crs_ids = set(doc_bt_dmd_crs.values_list('id_boite', flat=True))
    lst_doc_dmd = Demande.objects.filter(id_demandeur=id_user)
    restricted_doc_dmd_ids = set(lst_doc_dmd.values_list('id_docuement', flat=True))
    bt_dmd = Demande.objects.filter(id_boite=bte)
    bt_dmd_ids = set(bt_dmd.values_list('id_boite', flat=True))


    lst_doc = Document.objects.filter(id_boite=bte)

    data = []

    for doc in lst_doc:
        if Demande.objects.filter(id_boite=bte).exists():
            doc.bt = 1
        else:
            doc.bt = 0
        if Demande.objects.filter(id_docuement=doc.id_document, id_demandeur=id_user, date_retour__isnull=True,
                                  etat__in=[0, 1]).exists():
            doc.cons = 1
        else:
            doc.cons = 0

        if doc.id_document in restricted_doc_bt__ids:
            doc.disp = 0
        else:
            doc.disp = 1

        if doc.id_document in restricted_doc_ids:
            docres = RestrictionDocument.objects.get(id_doc=doc.id_document, id_user=id_user)
            doc.ref = docres.ref
            doc.dmd = docres.dmd
            doc.acces = 0
            doc.etat = 1
        else:
            doc.acces = 1
            doc.ref = 10
            doc.dmd = 10

            doc.etat = 10


        data.append({
            'id': doc.id_document,
            'bl': doc.bl,
            'date_creation': format(doc.date_creation, 'd F Y'),
            'client': doc.client,
            'eta': format(doc.eta, 'd F Y') ,
            'nom_navire': doc.nom_navire,
            'numero_voyage': doc.numero_voyage,
            'dmd': doc.dmd,
            'acces': doc.acces,
            'etat': doc.etat,
            'ref': doc.ref,
            'bt': doc.bt,
            'cons': doc.cons,
            'disp': doc.disp,

            'numero_document': doc.numero_docuemnt,
            # ... other fields
        })

    return JsonResponse({'data': data})


def fetch_boite(request, id):
        id_user = request.GET.get('id_user')
        if id_user:
            id_user = int(id_user)
        user = Utilisateurs.objects.get(id_utilisateur=id_user)
        direction = user.direction
        listuser = Utilisateurs.objects.filter(direction=direction)
        lst_dt_dmd = Demande.objects.filter(id_demandeur=id_user, date_retour__isnull=True, etat__in=[0, 1])
        restricted_doc_ids = set(lst_dt_dmd.values_list('id_boite', flat=True))
        bt_rg=Boite.objects.filter(id_user__in=listuser,numero_rang__startswith='Auc')
        rgbt_ids = set(bt_rg.values_list('id_boite', flat=True))
        data = []
        lisboite = Boite.objects.filter(id_user__in=listuser)
        for bt in lisboite:
            if bt.id_boite in restricted_doc_ids:
                bt.cons = 1
            else:
                bt.cons = 0
            if bt.id_boite in rgbt_ids:
                bt.rg = 1
            else:
                bt.rg = 0
            data.append({
                'id': bt.id_boite,
                'cons': bt.cons,
                'rg': bt.rg,
                'etat':bt.etat,
                'mention': bt.mention,
                #'date_creation': bt.date_creation,
                'date_creation': format( bt.date_creation, 'd F Y'),

            })

        return JsonResponse({'data': data})


        #return render(request, 'templatetra/list_boite.html', {'boite': lisboite, 'user': user, 'util': user})



def fect_tout_doc(request, id):
    id_user = request.GET.get('id_user')
    if id_user:
        id_user = int(id_user)
    # listedoc=Document.objects.all()
    listedoc = Document.objects.exclude(numero_docuemnt__startswith='CAT')
    user = Utilisateurs.objects.get(id_utilisateur=id_user)
    listeuser = Utilisateurs.objects.filter(direction=user.direction)
    boite = Boite.objects.filter(id_user__in=listeuser)
    ####document meeme direction
    docuser = Document.objects.filter(id_boite__in=boite)
    #####liste des documents restreintre
    listres = RestrictionDocument.objects.filter(id_user=id_user)
    ###############Liste des Docuemnts
    listresdmd = RestrictionDocument.objects.filter(id_user=id_user, etat=0)

    restricted_doc_ids = set(listres.values_list('id_doc', flat=True))
    list_doc_direction = set(docuser.values_list('id_document', flat=True))
    list_doc_dmd = set(listresdmd.values_list('id_doc', flat=True))
    lst_doc_dmd = Demande.objects.filter(id_demandeur=id_user)
    restricted_doc_dmd_ids = set(lst_doc_dmd.values_list('id_docuement', flat=True))
    ######boite  ranger
    lisboite_rg = Boite.objects.exclude(numero_rang__startswith='Auc')
    boite_range = set(lisboite_rg.values_list('id_boite', flat=True))
    ######boit occupe
    ######doc occupe
    lisboite_occupe = Demande.objects.filter(id_demandeur=id_user, etat__in=[0, 1], date_retour__isnull=True)
    doc_occupe = set(lisboite_occupe.values_list('id_docuement', flat=True))
    # Ajouter dynamiquement l'attribut 'acces=0' aux documents restreints dans listedoc
    data=[]
    for doc in listedoc:
        if doc.id_document in doc_occupe:
            doc.occ = 1
        else:
            doc.occ = 0

        if doc.id_boite in boite_range:
            doc.rg = 1
        else:
            doc.rg = 0
        if doc.id_document in restricted_doc_dmd_ids:
            doc.cons = 0
        else:
            doc.cons = 1
        if doc.id_document in list_doc_direction:
            doc.dir = 1
            #doc.per = 1

        else:
            doc.dir = 0
            doc.per = 1

        if doc.id_document in restricted_doc_ids:
            docres = RestrictionDocument.objects.get(id_doc=doc.id_document, id_user=id_user)
            doc.ref = docres.ref
            doc.dmd = docres.dmd
            doc.accept_dir = docres.acces_dir
            doc.acces = 0
            doc.etat = 1
            doc.acces_dir = docres.acces_dir
            doc.per = 0
        else:
            doc.acces = 1
            doc.per = 1
            doc.ref = 10
            doc.dmd = 10
            doc.accept_dir = 10
            doc.acces_dir=10

            doc.etat = 1
            doc.per = 1
        docuser = Document.objects.get(id_document=doc.id_document)
        btuser = Boite.objects.get(id_boite=docuser.id_boite)
        useru = Utilisateurs.objects.get(id_utilisateur=btuser.id_user)
        doc.direction = useru.direction

        data.append({
        'id': doc.id_document,
        'bl': doc.bl,
        'date_creation': format(doc.date_creation, 'd F Y'),
        'client': doc.client,

            'eta': format(doc.eta, 'd F Y'),
        'nom_navire': doc.nom_navire,
        'numero_voyage': doc.numero_voyage,
        'dmd': doc.dmd,
        'acces': doc.acces,
        'etat': doc.etat,
            'acces_dir' : doc.acces_dir,
        'ref': doc.ref,
        'occ': doc.occ,
        'cons': doc.cons,
        'per': doc.per,
        'rg': doc.rg,
        'dir': doc.dir,
            'direction' :  doc.direction,

        'numero_document': doc.numero_docuemnt,
        # ... other fields
    })

    return JsonResponse({'data': data})


def fetch_permission(request, id):
    id_user = request.GET.get('id_user')
    if id_user:
        id_user = int(id_user)
    user = Utilisateurs.objects.get(id_utilisateur=id_user)
    lstuser = Utilisateurs.objects.filter(direction=user.direction)
    listboit = Boite.objects.filter(id_user__in=lstuser)
    listdoc = Document.objects.filter(id_boite__in=listboit)
    Liste_user = Utilisateurs.objects.all()
    #####document no direction
    documents_no_dir = Document.objects.exclude(id_document__in=listdoc.values_list('id_document', flat=True))

    # lisrect=RestrictionDocument.objects.filter(id_doc__in=listdoc,ref=0)
    lisrect = RestrictionDocument.objects.filter(id_chef=id_user, ref=0, acces_dir=1)
    restricted_ids_doc = set(listdoc.values_list('id_document', flat=True))
    restricted_ids_user = set(Liste_user.values_list('id_utilisateur', flat=True))
    lstdoc_no_dir = set(documents_no_dir.values_list('id_document', flat=True))
    # Ajouter dynamiquement l'attribut 'acces=0' aux documents restreints dans listedoc
    ####doc direction
    us = Utilisateurs.objects.get(id_utilisateur=id_user)
    lsuserdir = Utilisateurs.objects.filter(direction=us.direction)
    btdir = Boite.objects.filter(id_user__in=lsuserdir)
    docdir = Document.objects.filter(id_boite__in=btdir)
    lstdocdir = set(docdir.values_list('id_document', flat=True))
    data=[]
    for doc in lisrect:

        user = Utilisateurs.objects.get(id_utilisateur=id_user)
        if doc.service == user.direction:
            doc.mdir = 1
        else:
            doc.mdir = 0

        if doc.id_doc in restricted_ids_doc:
            doc.dir = 1
            docu = Document.objects.get(id_document=doc.id_doc)
            # doc.document=docu.chemin_acces
            if doc.id_user in restricted_ids_user:
                useru = Utilisateurs.objects.get(id_utilisateur=doc.id_user)
                doc.document = docu.chemin_acces
                doc.numero = docu.numero_docuemnt
                doc.user = useru.prenom + ' ' + useru.nom
                doc.direction = user.direction
        if doc.id_doc in lstdoc_no_dir:
            doc.dir = 0
            docu = Document.objects.get(id_document=doc.id_doc)
            # doc.document=docu.chemin_acces

            if doc.id_user in restricted_ids_user:
                useru = Utilisateurs.objects.get(id_utilisateur=doc.id_user)
                doc.document = docu.chemin_acces
                doc.numero = docu.numero_docuemnt
                doc.user = useru.prenom + ' ' + useru.nom
                doc.direction = user.direction
        data.append({
            'id': doc.id_doc,
            'id_res': doc.id_restric,
            'numero_document': doc.numero,
            'useru':doc.user,
            'mdir': doc.mdir,
            'dir':doc.dir,

            # ... other fields
        })

    return JsonResponse({'data': data})

    #return render(request, 'templatetra/liste_permission.html', {'lstres': lisrect, 'util': user})


def fecth_demande(request, id):
    id_user = request.GET.get('id_user')
    if id_user:
        id_user = int(id_user)
    user = Utilisateurs.objects.get(id_utilisateur=id_user)
    dmd = Demande.objects.filter(date_retour__isnull=True, etat__in=[0, 1])
    lsdmandeur = Utilisateurs.objects.filter(id_utilisateur__in=dmd)
    lsdoc = Document.objects.filter(id_document__in=dmd)
    lsboite = Boite.objects.filter(id_boite__in=dmd)
    restricted_doc_ids = set(lsdoc.values_list('id_document', flat=True))
    restricted_userr_ids = set(lsdmandeur.values_list('id_utilisateur', flat=True))
    restricted_boite_ids = set(lsboite.values_list('id_boite', flat=True))
    ###retour
    dmd_accepte = Demande.objects.filter(etat=1, date_retour__isnull=True)
    dmd_accepte_ids = set(dmd_accepte.values_list('id_dmd', flat=True))
    #####Accepter
    # dmd_attente = Demande.objects.filter(id_accepteur__isnull=True)
    # dmd_attente_ids = set(dmd_attente.values_list('id_dmd', flat=True))
    data=[]
    for doc in dmd:
        if doc.id_dmd in dmd_accepte_ids:
            doc.ret = 1
        else:
            doc.ret = 0

        if doc.type == "document":
            doc.bt = 0
            user = Utilisateurs.objects.get(id_utilisateur=doc.id_demandeur)
            doc.numero = Document.objects.get(id_document=doc.id_docuement).numero_docuemnt
            doc.user = user.nom + user.prenom
            dmd_attente_boite = Demande.objects.filter(date_retour__isnull=True, etat=1, id_docuement=doc.id_docuement)
            dmd_attente_boite_ids = set(dmd_attente_boite.values_list('id_docuement', flat=True))
            if doc.id_docuement in dmd_attente_boite_ids:
                doc.att = 1
            else:
                doc.att = 0
            if doc.id_docuement in restricted_doc_ids:
                dmd_attente_boite = Demande.objects.filter(date_retour__isnull=True, etat=1,
                                                           id_docuement=doc.id_docuement)
                dmd_attente_boite_ids = set(dmd_attente_boite.values_list('id_docuement', flat=True))
                if doc.id_docuement in dmd_attente_boite_ids:
                    doc.att = 1
                else:
                    doc.att = 0

                if doc.id_docuement in restricted_doc_ids:
                    if doc.id_demandeur in restricted_userr_ids:
                        user = Utilisateurs.objects.get(id_utilisateur=doc.id_demandeur)
                        doc.numero = Document.objects.get(id_document=doc).numero_docuemnt
                        doc.user = user.nom + user.prenom
        else:
            doc.bt = 1
            user = Utilisateurs.objects.get(id_utilisateur=doc.id_demandeur)
            doc.numero = Boite.objects.get(id_boite=doc.id_boite).mention
            doc.user = user.nom + user.prenom
            dmd_attente_boite = Demande.objects.filter(date_retour__isnull=True, etat=1, id_boite=doc.id_boite)
            dmd_attente_boite_ids = set(dmd_attente_boite.values_list('id_boite', flat=True))
            if doc.id_boite in dmd_attente_boite_ids:
                doc.att = 1
            else:
                doc.att = 0
            if doc.id_boite in restricted_boite_ids:
                user = Utilisateurs.objects.get(id_utilisateur=doc.id_demandeur)
                doc.numero = Boite.objects.get(id_boite=doc.id_boite).mention
                doc.user = user.nom + user.prenom
                if doc.id_demandeur in restricted_userr_ids:
                    user = Utilisateurs.objects.get(id_utilisateur=doc.id_demandeur)
                    doc.numero = Boite.objects.get(id_boite=doc.id_boite).mention
                    doc.user = user.nom + user.prenom
        data.append({
            'id': doc.id_dmd,

            'numero_document': doc.numero,
            'ret':doc.ret,
            'bt': doc.bt,
            'att': doc.att,
            'numero':doc.numero,
            'user' :doc.user,
            'type' : doc.type,
            'date_creation' : format(doc.date_dmd, 'd F Y'),
            'commentaire' :doc.commentaire,

            # ... other fields
        })
    return JsonResponse({'data': data})

def fetchboiteAclasser(request, id):
        boite = Boite.objects.filter(etat=0, numero_rang__startswith='Aucune')
        #user = Utilisateurs.objects.get(id_utilisateur=id)
        data = []
        for doc in boite:
            data.append({
            'id': doc.id_boite,
            'etat' : doc.etat,
            'mention': doc.mention,
            'date_creation': format(doc.date_creation, 'd F Y'),

            })
        return JsonResponse({'data': data})

        # return render(request, 'docs/listeboiteclasser.html', {'doc': boite, 'user': user, 'util': user})

        #return render(request, 'templatetra/liste_boite_cloture.html', {'boite': boite, 'user': user, 'util': user})

    #useru = Utilisateurs.objects.get(id_utilisateur=id_user)
    #return render(request, 'templatetra/list_demande.html', {'util': useru, 'dmd': dmd})


def fetch_global_doc(request, id):
    id_user = request.GET.get('id_user')
    if id_user:
        id_user = int(id_user)
    # listedoc=Document.objects.all()
    listedoc = Document.objects.exclude(numero_docuemnt__startswith='CAT')
    ######boite  ranger
    lisboite_rg = Boite.objects.exclude(numero_rang__startswith='Auc')
    boite_range = set(lisboite_rg.values_list('id_boite', flat=True))
    ######doc occupe
    lisboite_occupe = Demande.objects.filter(id_demandeur=id_user, etat__in=[0, 1], date_retour__isnull=True)
    doc_occupe = set(lisboite_occupe.values_list('id_docuement', flat=True))
    # Ajouter dynamiquement l'attribut 'acces=0' aux documents restreints dans listedoc
    data=[]
    for doc in listedoc:
        if doc.id_document in doc_occupe:
            doc.occ = 1
        else:
            doc.occ = 0

        if doc.id_boite in boite_range:
            doc.rg = 1
        else:
            doc.rg = 0
        docuser=Document.objects.get(id_document=doc.id_document)
        btuser=Boite.objects.get(id_boite=docuser.id_boite)
        useru=Utilisateurs.objects.get(id_utilisateur=btuser.id_user)
        doc.direction=useru.direction
        data.append({
        'id': doc.id_document,
        'bl': doc.bl,
        'date_creation': format(doc.date_creation, 'd F Y'),
        'client': doc.client,
        'eta': format(doc.eta, 'd F Y'),
            'direction':doc.direction,

        'nom_navire': doc.nom_navire,
        'numero_voyage': doc.numero_voyage,
        'occ': doc.occ,
        'rg': doc.rg,
            'numero_document' : doc.numero_docuemnt,
    })

    return JsonResponse({'data': data})

    #user = Utilisateurs.objects.get(id_utilisateur=id)

    #return render(request, 'templatetra/document_global_manage.html', {'util': user, 'doc': listedoc})
def fretch_mes_demandes(request, id):
    id_user = request.GET.get('id_user')
    if id_user:
        id_user = int(id_user)
    user = Utilisateurs.objects.get(id_utilisateur=id_user)
    res = RestrictionDocument.objects.filter(id_user=id_user,dmd=1,acces_dir__in=[1,2])
    data = []
    for doc in res:
        data.append({

            'numero_document': doc.numero_docuent,
               'service' : doc.service,
           'date_dmd' : format(doc.date_dmd , 'd F Y'),
             'etat' :   doc.etat,
            'dmd': doc.dmd,
            'ref': doc.ref,
            'acces_dir': doc.acces_dir,
            'acces': doc.acces,

        })

    return JsonResponse({'data': data})

def fetch_mes_consultations(request, id):
    id_user = request.GET.get('id_user')
    if id_user:
        id_user = int(id_user)
    dmd = Demande.objects.filter(id_demandeur=id_user)
    user = Utilisateurs.objects.get(id_utilisateur=id_user)
    data = []
    for doc in dmd :
        data.append({

            'type' : doc.type,
        'commentaire':doc.commentaire,
        'date_dmd' : format(doc.date_dmd, 'd F Y'),
        'etat' : doc.etat,
        'commentaire_reponse' : doc.commentaire_reponse,

        })

    return JsonResponse({'data': data})
        #return render(request, 'templatetra/mes_demandes_consultations.html', {'cons': dmd, 'util': user})

    #return render(request, 'templatetra/mes_demandes.html', {'lstres': res, 'util': user})





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
