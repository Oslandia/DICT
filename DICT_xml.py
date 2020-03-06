#!/usr/bin/env python
# -*- coding:utf-8 -*-

from xml.dom import minidom
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import QMessageBox
from .DICT_geometrie import DICT_geometrie
from .DICT_dialog_wizard import DICTDialogWizard

from dateutil import parser
import tempfile
import os
import sys
import datetime
import subprocess

class DICT_xml(object):
    def __init__(self, xml_file):
        msgBox = QMessageBox()
        msgBox.setTextFormat(Qt.RichText)

        try:
            self._xmldoc = minidom.parse(xml_file)
        except IOError:
            msgBox.setText("Fichier XML introuvable.")
            msgBox.exec_()
            return

        try:
            (self._rc_pref, self._gml_tag,
            self._gml_alt_tag, self._geom_tag) = self.__initTag()
            self._taillePlan = self.__findFormatPlan()
            self._attributs = self.__createAttributs()
        except:
            msgBox.setText("Erreur de lecture du fichier XML.")
            msgBox.exec_()
            return

        #try:
        # Dessine la géométrie
        self.geom = DICT_geometrie(self._xmldoc, self._geom_tag, self._gml_tag, self._gml_alt_tag)
        self.geom.addGeometrie()
        #except:
        #    msgBox.setText("Erreur lors de la génération de la géométrie.")
         #   msgBox.exec_()
          #  return

    def __initTag(self):
        rc_base = 'http://www.reseaux-et-canalisations.gouv.fr/' + \
                  'schema-teleservice/'
        rc1 = rc_base + '2.1'
        rc2 = rc_base + '2.2'
        rc3 = rc_base + '3.0'
        gml = 'http://www.opengis.net/gml/3.2'

        l = []
        for j in list(self._xmldoc.documentElement.attributes.items()):
            l.append(j[0]), l.append(j[1])

        rc = None
        if rc1 in l:
            rc = rc1
        elif rc2 in l:
            rc = rc2
        elif rc3 in l:
            rc = rc3

        gml_index = l.index(gml)-1
        rc_index = l.index(rc)-1

        gml_pref, rc_pref = "", ""
        gml_pref_ind = l[gml_index].find(':')
        if gml_pref_ind != -1:
            gml_pref = l[gml_index][gml_pref_ind+1:]+":"

        rc_pref_ind = l[rc_index].find(':')
        if rc_pref_ind != -1:
            rc_pref = l[rc_index][rc_pref_ind+1:]+":"

        gml = gml_pref + "coordinates"
        gml_alt = gml_pref + "posList"
        geom = rc_pref + "geometrie"

        return rc_pref, gml, gml_alt, geom

    def __findFormatPlan(self):
        recepElec = self._xmldoc.getElementsByTagName(self._rc_pref +
                                             "modeReceptionElectronique")
        formatPlan = self.__extraitAttr(recepElec, "tailleDesPlans")

        if formatPlan != "":
            return formatPlan
        else:
            return "A4"

    def __extraitAttr(self, xml, attribut):
        ext = self._rc_pref
        try:
            att = xml[0].getElementsByTagName(self._rc_pref + attribut)
            return att[0].firstChild.nodeValue
        except:
            return ""

    def __createAttributs(self):
        xml = self._xmldoc
        dico = {}

        # DT DICT
        dico['Recepisse_DC'] = False
        dico['Recepisse_DICT'] = False
        dico['Recepisse_DT'] = False
        typed = ""
        if xml.getElementsByTagName(self._rc_pref + 'dtDictConjointes'):
            typed = self._rc_pref + 'dtDictConjointes'
            dico['Recepisse_DC'] = True
        elif xml.getElementsByTagName(self._rc_pref + 'DT'):
            typed = self._rc_pref + 'DT'
            dico['Recepisse_DT'] = True
        elif xml.getElementsByTagName(self._rc_pref + 'DICT'):
            typed = self._rc_pref + 'DICT'
            dico['Recepisse_DICT'] = True
        else:  # ATU
            return

        #
        # Consultation
        #
        dest = xml.getElementsByTagName(typed)

        # Numéro de consultation (soit normal soit à seize)
        recep_NumCons = self.__extraitAttr(dest, "noConsultationDuTeleservice")
        if len(recep_NumCons) == 0:
            recep_NumCons = self.__extraitAttr(dest, "noConsultationDuTeleserviceSeize")
        dico['NoGu'] = recep_NumCons

        # Numéro d'affaire
        recep_NumAff = self.__extraitAttr(dest, "noAffaireDeLexecutantDesTravaux")
        dico['NoAffaireDeclarant'] = recep_NumAff

        # Personne à contacter (déclarant)
        recep_RespProjet = self.__extraitAttr(dest, "nomDeLaPersonneAContacter")
        dico['Personne_Contacter'] = recep_RespProjet

        # Date de réception
        recep_DateRec = self.__extraitAttr(dest, "dateDeLaDeclaration")
        dateRecep = parser.parse(recep_DateRec)
        dico['JourReception'] = str(dateRecep.day).rjust(2, '0')
        dico['MoisReception'] = str(dateRecep.month).rjust(2, '0')
        dico['AnneeReception'] = str(dateRecep.year).rjust(4)
        dico['dateRecep'] = dateRecep

        # Commune principale
        recep_Commune = self.__extraitAttr(dest, "communePrincipale")
        dico['communePrincipale'] = recep_Commune

        # Adresse des travaux
        recep_Adresse = self.__extraitAttr(dest, "adresse")
        dico['AdresseTravaux'] = recep_Adresse

        # Référence de l'exploitant à incrémenter
        num = "000000"
        configExt = QSettings().value("/DICT/configExtension")
        if configExt is None:
            configExt = ''
        recep_Ref = datetime.date.today().strftime("%Y")+configExt+num
        dico['ReferenceExploitant'] = recep_Ref

        #
        # Destinataire
        #
        if dico['Recepisse_DT']:
            dest = xml.getElementsByTagName(
                                self._rc_pref +
                                'representantDuResponsableDeProjet')
        else:
            dest = xml.getElementsByTagName(self._rc_pref +
                                            'executantDesTravaux')

        dest_Denomination = self.__extraitAttr(dest, "denomination")
        dico['dest_Denomination'] = dest_Denomination

        dest_ComplementAdresse = self.__extraitAttr(dest, "complementService")
        dico['dest_ComplementAdresse'] = dest_ComplementAdresse

        dest_NoVoie = self.__extraitAttr(dest, "numero") + " " + \
           self.__extraitAttr(dest, "voie")

        dico['dest_NoVoie'] = dest_NoVoie

        dest_LieuditBP = self.__extraitAttr(dest, "lieuDitBP")
        dico['dest_LieuditBP'] = dest_LieuditBP

        dest_CodePostal = self.__extraitAttr(dest, "codePostal")
        dico['dest_CodePostal'] = dest_CodePostal

        dest_Commune = self.__extraitAttr(dest, "commune")
        dico['dest_Commune'] = dest_Commune

        dest_Pays = self.__extraitAttr(dest, "pays")
        dico['dest_Pays'] = dest_Pays

        return dico

    def formulaire(self, exportPDF=True):
        # Afficher un assistant de saisie
        dlgWizard = DICTDialogWizard(self._attributs)
        dlgWizard.show()
        result = dlgWizard.exec_()
        if result and exportPDF:
            titre, pdf = None, None
            if QSettings().value("/DICT/formPoppler") is True:
                titre, pdf = dlgWizard.saveChangePoppler()
            else:
                titre, pdf = dlgWizard.saveChangeQGis()

            return titre, pdf

    def geometriePDF(self, titre):
        return self.geom.geometriePDF(titre, self._taillePlan)
