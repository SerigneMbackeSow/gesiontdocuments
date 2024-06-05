from django.urls import path

from .views import *

class Listearchiveboite:
    pass


urlpatterns = [
    path('seconnecter/', login_page, name='seclogin'),
    #path('enregistreutilisateur/', Crer_Utilisateur_page, name='Crer_utilisateur'),
    path('enregistrerutilisateur/', enregistrer_Utilisateur, name='logout'),
    path('crerutilisateur', Crer_Utilisateur_page, name='logout'),
    ########################Gestion Agent
    path('listeagent/<int:id>',list_agent, name='listearchive'),
    path('crer_agent_page/<int:id>', Crer_agent_page, name='listearchive'),
    path('enregistreragent/', enregistrer_agent, name='listearchive'),
    path('update_page/<int:id_user>/<int:id_agt>', update_agent_page, name='listearchive'),
    path('enregistrer_upadte_agent/', upadte_agent, name='listearchive'),
    path('desactiver/<int:id_user>/<int:id_agt>', desactiver_agent, name='listearchive'),
    path('activer/<int:id_user>/<int:id_agt>', activer_agent, name='listearchive'),
    path('reinitipass/<int:id_user>/<int:id_agt>/', reinitiliaser_mdp, name='listearchive'),
    ####################Gestion Demande
    path('demandeboite/<int:id>/<int:id_boite>', demande_acces_boite, name='listearchive'),
    path('enregistrer_demande_boite/',enregistrer_demande_boite, name='listearchive'),
    path('demandedoc/<int:id>/<int:id_doc>', demande_acces_document, name='listearchive'),
    path('enregistrer_demande_doc/',enregistrer_demande_doc, name='listearchive'),
    path('voir_document_demande/<int:id_user>/<int:id_doc>', voire_document_demande, name='listearchive'),

    #############Gestion demane Tout
    path('demandedoc_tout/<int:id>/<int:id_doc>', demande_acces_document_tout, name='listearchive'),
    path('enregistrer_demande_doc_tout/',enregistrer_demande_doc_tout, name='listearchive'),
    path('demandepermission_tout/<int:id>/<int:id_doc>',demandepermission_tout, name='listearchive'),
    path('demandepermission_direction/<int:id>/<int:id_doc>',demandepermission_tout_direction, name='listearchive'),

    #########Gestion deamnde Archoive
    path('listedmd/<int:id>', liste_demande, name='listearchive'),
    path('refuse_dmd_page/<int:id>/<int:id_dmd>', refusd_demande_page, name='listearchive'),
    path('enregistrer_refut/', enregistrer_demande_refut, name='listearchive'),
    path('accepter_dmd/<int:id>/<int:id_dmd>', enregistrer_demande_acept, name='listearchive'),
    #####################Gestion Permission
    path('refuse_page/<int:id>/<int:id_doc>', retriction_page, name='listearchive'),
     path('retriction/',enregistrer_restriction,name='listearchive'),
    ####################Gestion Permisio Tout
    #####################Gestion Permission
    path('refuse_page/<int:id>/<int:id_doc>', retriction_page, name='listearchive'),
    path('retriction/', enregistrer_restriction, name='listearchive'),

    #######################Gestion Permission tout
    path('retrindre_page_tout/<int:id>/<int:id_doc>',  retriction_page_tout, name='listearchive'),
    path('retriction_tout/', enregistrer_restriction_tout, name='listearchive'),








    #####################GESTION BOITE
    path('listeboite/<int:id>', listeboitedirection, name='listearchive'),
    path('ajouterboite_page/<int:id>', ajouterboite_page, name='listearchive'),
    path('enregistrerboite/',enregistrerboite,name='listearchive'),
    path('listedocumentboite/<int:id>/<int:id_user>',listedocumentboite,name='listearchive'),
    path('clotureBoite/<int:id>',clotureBoite,name='listearchive'),
    path('ajouterdocument/<int:id>',ajouterdossier_page,name='listearchive'),
    path('ajouterdocument/',ajouterdocumentboite,name='listearchive'),
    path('cloturer/<int:id>',clotureBoite,name='listearchive'),
    path('voiredetail/<int:id>/<int:id_user>',voir_detail_boite,name='listearchive'),
    path('updateboite/',updateboite,name='listearchive'),
    path('voirdoc/<int:id>/<int:id_user>',voire_document,name='listearchive'),
    ##########Archiviste###########################
    path('liste_boite_cloture/<int:id>', listeboiteAclasser, name='listearchive'),
    path('liste_boite_classer/<int:id>/<int:id_user>', classerBoite_page, name='listearchive'),
    path('classer_boite/', classerboite, name='listearchive'),
    path('detail_boite/<int:id>/<int:id_user>', voir_detail_archive, name='listearchive'),
    path('upadteboitearchivie/',updateboite_archiviste, name='listearchive'),
    path('liste_boite_classes/<int:id>', listeboiteclasser, name='listearchive'),
    path('tot_document/<int:id>', tout_doc, name='listearchive'),
    path('voir_tout_document/<int:id>/<int:id_user>',voir_tout_document, name='listearchive'),

    ##############################################Gestion des chefs de services
    path('listechef/<int:id>', list_chef, name='listearchive'),
    path('crer_chef_page/<int:id>', Crer_chef_page, name='listearchive'),
    path('enregistrerchef/', enregistrer_chef, name='listearchive'),
    path('update_page_chef/<int:id_user>/<int:id_chf>', update_chef_page, name='listearchive'),
    path('enregistrer_upadte_chef/', upadte_chef, name='listearchive'),
    path('desactiver/<int:id_user>/<int:id_chf>', desactiver_chef, name='listearchive'),
    path('activer_chef/<int:id_user>/<int:id_chf>', activer_chef, name='listearchive'),
    path('reinitipass_chef/<int:id_user>/<int:id_chf>/', reinitiliaser_mdp_chef, name='listearchive'),
    ######GESTION Restriction###########################
    path('liste_permission/<int:id>', listpermission, name='listearchive'),
    path('dmd_permission/<int:id>/<int:id_doc>/<int:id_boite>', demandepermission, name='listearchive'),
    path('accepter_per/<int:id>/<int:id_user>', acceptr_permission, name='listearchive'),
    path('refuser_per/<int:id>/<int:id_user>', refuser_permission, name='listearchive'),

    path('dmd_permission_tout/<int:id>/<int:id_doc>', demandepermission_tout, name='listearchive'),


    #######################ARCHIVE##########################
    path('listeboiteaclasser/<int:id>',listeboiteAclasser,name='listearchive'),
    path('listedemesddemande/<int:id>',listedemesddemandeConsultation,name='listearchive'),

    ###################GESTION DES DEMENADES AGENTs
    path('liste_mes_demnades/<int:id>',mes_demandes,name='listearchive'),





    ######################GESTION CONSULTATION
     path('liste_consultation/<int:id>',mes_consultations,name='listearchive'),
    ##############################Gestion voir detail Consultation
    path('detail_docu_con/<int:id>/<int:id_user>',voir_detail_document_consultation,name='listearchive'),
    path('detail_boite_con/<int:id>/<int:id_user>',voir_detail_boite_consultation,name='listearchive'),

]
