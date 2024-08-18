from django.urls import path

from .views import *

urlpatterns = [

    ############Test Archive
    path('testarchive/<int:id_user>', testarchive, name='testarchive'),
    path('ajouter_dossier/', ajouter_dossier, name='ajouter_dossier'),
    path('liste_dossier/<int:id_user>/<int:id_prt>', liste_dossier, name=' liste_dossier'),
    path('dossier_racine/<int:id_user>', dossier_racine, name='dossier_racine'),
    ###########Gestion Document
    path('ajouter_document/', ajouterdocument, name='ajouterdocument'),
    path('affiche_document/<int:id_user>/<int:id_doc>', affiche_document, name=' affiche_document'),
    path('affiche_document_tout/<int:id_user>/<int:id_doc>', affiche_document_tout, name=' affiche_document'),
    ####Gestrion Restriction
    path('ajout_acces/', ajout_acces, name='ajout_acces'),
    path('restraindre_page/<int:id_user>/<int:id_objet>/<str:type>', restraindre_page, name='restraindre_page'),

    path('restraindre_page_toout/<int:id_user>/<int:id_objet>/<str:type>', restraindre_page_tout, name='restraindre_page'),
    ###############Gestion demande Permission
    path('ajouter_permission/', ajout_demande, name='ajout_demande'),
    path('demande_permission_recue/<int:id_user>', demande_permission_recus, name='demande_permission_recu'),
    path('fetch_demande_acces/<int:id_user>', fetch_demande_acces, name='fetch_demande_acces'),
    path('accepter_dmd/<int:id_dmd>/<int:id_user>', accepter_dmd, name='accepter_dmd'),
    path('refuser_dmd/', refuser_dmd, name='accepter_dmd'),
    path('demande_permission_envoyes/<int:id_user>', demande_permission_envoyes, name='demande_permission_envoy'),
    path('fetch_mes_demandes_envoyer/<int:id_user>', fetch_demande_acces_envoyes, name='fetch_demande_acces_envoyes'),
    path('fetch_arborescence/<int:id_docrt>', fetch_arborescence, name='fetch_arborescence'),
    #######################Gestion Utilisateur
    path('gestion_utilsateurs/<int:id_user>', gestion_utilsateurs, name='gestion_utilsateurs'),
    path('ajouter_utilisateur/', ajouter_utilisateur, name='ajouter_utilisateur'),
    path('activer/<int:id_user>', activer_utilisateur, name='activer'),
    path('desactiver/<int:id_user>', desactiver_utilisateur, name='desactiver'),
    path('reinitialiser_utilisateur/<int:id_user>', reinitialiser_utilisateur, name='reinitialiser_utilisateur'),

    path('update_utilisateur/', update_utilisateur, name='update_utilisateur'),


    ##############Gestion tout dossier
    path('tout_dossier_admin/<int:id_user>', tout_dossier_admin, name='tout_dossier_admin'),
    path('liste_dossier_admin/<int:id_user>/<int:id_dos>', liste_dossier_admin, name='liste_dossier_admin'),
    path('modifier_dossier/', modifier_dossier, name='modifier_dossier'),
    path('modifier_dossier_direction/', modifier_dossier_direction, name='modifier_dossier_direction'),
    ############Gestion Management
    path('liste_tout_document/<int:id_user>', liste_tout_document, name='liste_tout_document'),
    path('fetch_documents/', fetch_documents, name='fetch_documents'),
    ###########Edit Document
    path('edit_document/<int:id_user>/<int:id_doc>', edit_document, name='edit_document'),
    path('enregistrer_document/', sauvegarde_contenu_document, name='sauvegarde_contenu_document'),
    ######## Update Document
    path('update_document/', update_document, name='update_document'),
    #path('get_descendants', get_descendants_data, name='get_descendants_data'),
    ########Fetch dossier
    path('fetch_dossiers/', fetch_dossiers_tout, name='fetch_dossiers'),
    ###########tout_document_ direction
    path('liste_document_direction/<int:id_user>', liste_tout_direction, name=' liste_dossier'),
path('fetch_dossiers_direction/', fetch_dossiers_tout_direction, name='fetch_dossiers_direcction'),
    #################Rediurection
path('redirige_app/<str:app>', redirige_app, name='redirige_app'),
    #######################  FONCTION POUR LA MODIFICATION DU MOT DE PASE
    path('profile/<int:id_user>', profile_page, name='profile_page'),
    path('modifier_profile/', modifier_profile, name='modifier_profile'),
    path('retour_profile/<int:id_user>', retour_profile, name='retour_profil'),
]



