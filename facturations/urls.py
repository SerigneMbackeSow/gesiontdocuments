from django.urls import path

from .views import *

class Listearchiveboite:
    pass


urlpatterns = [
    path('seconnecter/', login_page, name='seclogin'),
    #path('enregistreutilisateur/', Crer_Utilisateur_page, name='Crer_utilisateur'),
    path('crerutilisateur/', Crer_Utilisateuwr_page, name='logout'),
    #####################GESTION BOITE
    path('listeboite/<int:id>', listeboitedirection, name='listearchive'),
    path('ajouterboite_page/<int:id>', ajouterboite_page, name='listearchive'),
    path('enregistrerboite/',enregistrerboite,name='listearchive'),
    path('listedocumentboite/<int:id>',listedocumentboite,name='listearchive'),
    path('clotureBoite/<int:id>',clotureBoite,name='listearchive'),
    path('ajouterdocument/<int:id>',ajouterdossier_page,name='listearchive')


]
