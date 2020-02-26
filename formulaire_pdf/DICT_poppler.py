# -*- coding: utf-8 -*-
"""
Created on Wed May 25 13:26:46 2016

@author: Loïc BARTOLETTI
"""
try:
    import popplerqt5
    POPPLER = True
except:
    POPPLER = False

from PyQt5.QtGui import *
from PyQt5.QtCore import *
from ..DICT_dialog_wizard import DICTDialogWizard

import os

# doc = popplerqt5.Poppler.Document.load('cerfa_14435-03.pdf')
# page = doc.page(0)
# fields = page.formFields()
# Tous les ids du cerfa 14435-03 commencent par un increment à 65536
# l = [(f.id()-65536, f.name(), f.type()) for f in fields]
#
# [(0, PyQt4.QtCore.QString(u'Recepisse_DT'), 0),
# (1, PyQt4.QtCore.QString(u'Recepisse_DICT'), 0),
# (2, PyQt4.QtCore.QString(u'Recepisse_DC'), 0),
# (3, PyQt4.QtCore.QString(u'Denomination'), 1),
# (4, PyQt4.QtCore.QString(u'ComplementAdresse'), 1),
# (5, PyQt4.QtCore.QString(u'NoVoie'), 1),
# (6, PyQt4.QtCore.QString(u'LieuditBP'), 1),
# (7, PyQt4.QtCore.QString(u'CodePostal'), 1),
# (8, PyQt4.QtCore.QString(u'Commune'), 1),
# (9, PyQt4.QtCore.QString(u'Pays'), 1),
# (10, PyQt4.QtCore.QString(u'NoGu'), 1),
# (11, PyQt4.QtCore.QString(u'ReferenceExploitant'), 1),
# (12, PyQt4.QtCore.QString(u'NoAffaireDeclarant'), 1),
# (13, PyQt4.QtCore.QString(u'Personne_Contacter'), 1),
# (14, PyQt4.QtCore.QString(u'JourReception'), 1),
# (15, PyQt4.QtCore.QString(u'MoisReception'), 1),
# (16, PyQt4.QtCore.QString(u'AnneeReception'), 1),
# (17, PyQt4.QtCore.QString(u'CommuneTravaux'), 1),
# (18, PyQt4.QtCore.QString(u'AdresseTravaux'), 1),
# (19, PyQt4.QtCore.QString(u'RaisonSocialeExploitant'), 1),
# (20, PyQt4.QtCore.QString(u'ContactExploitant'), 1),
# (21, PyQt4.QtCore.QString(u'NoVoieExploitant'), 1),
# (22, PyQt4.QtCore.QString(u'LieuditBPExploitant'), 1),
# (23, PyQt4.QtCore.QString(u'CodePostalExploitant'), 1),
# (24, PyQt4.QtCore.QString(u'CommuneExploitant'), 1),
# (25, PyQt4.QtCore.QString(u'TelExploitant'), 1),
# (26, PyQt4.QtCore.QString(u'FaxExploitant'), 1),
# (27, PyQt4.QtCore.QString(u'RepImpossible'), 0),
# (28, PyQt4.QtCore.QString(u'InfoPreciser'), 1),
# (29, PyQt4.QtCore.QString(u'PasConcerne'), 0),
# (30, PyQt4.QtCore.QString(u'DistanceReseau'), 1),
# (31, PyQt4.QtCore.QString(u'Concerne'), 0),
# (32, PyQt4.QtCore.QString(u'CategorieReseau1'), 2),
# (33, PyQt4.QtCore.QString(u'CategorieReseau2'), 2),
# (34, PyQt4.QtCore.QString(u'CategorieReseau3'), 2),
# (35, PyQt4.QtCore.QString(u'ModifPrevue'), 1),
# (36, PyQt4.QtCore.QString(u'ModifEnCours'), 0),
# (37, PyQt4.QtCore.QString(u'RepresentantExploitant'), 1),
# (38, PyQt4.QtCore.QString(u'TelModification'), 1),
# (39, PyQt4.QtCore.QString(u'PlansJoints'), 0),
# (40, PyQt4.QtCore.QString(u'Ref1'), 1),
# (41, PyQt4.QtCore.QString(u'Echelle1'), 1),
# (42, PyQt4.QtCore.QString(u'JourEditionPlan1'), 1),
# (43, PyQt4.QtCore.QString(u'MoisEditionPlan1'), 1),
# (44, PyQt4.QtCore.QString(u'AnneeEdition1'), 1),
# (45, PyQt4.QtCore.QString(u'Sensible1'), 0),
# (46, PyQt4.QtCore.QString(u'Profondeur1'), 1),
# (47, PyQt4.QtCore.QString(u'Materiau1'), 1),
# (48, PyQt4.QtCore.QString(u'Ref2'), 1),
# (49, PyQt4.QtCore.QString(u'Echelle2'), 1),
# (50, PyQt4.QtCore.QString(u'JourEditionPlan2'), 1),
# (51, PyQt4.QtCore.QString(u'MoisEditionPlan2'), 1),
# (52, PyQt4.QtCore.QString(u'AnneeEdition2'), 1),
# (53, PyQt4.QtCore.QString(u'Sensible2'), 0),
# (54, PyQt4.QtCore.QString(u'Profondeur2'), 1),
# (55, PyQt4.QtCore.QString(u'Materiau2'), 1),
# (56, PyQt4.QtCore.QString(u'ReunionChantierCase'), 0),
# (57, PyQt4.QtCore.QString(u'DateRDV'), 0),
# (58, PyQt4.QtCore.QString(u'JourReunion'), 1),
# (59, PyQt4.QtCore.QString(u'MoisReunion'), 1),
# (60, PyQt4.QtCore.QString(u'AnneeReunion'), 1),
# (61, PyQt4.QtCore.QString(u'HeureReunion'), 1),
# (62, PyQt4.QtCore.QString(u'MinuteReunion'), 1),
# (63, PyQt4.QtCore.QString(u'RDVparDeclarant'), 0),
# (64, PyQt4.QtCore.QString(u'AppelNonConcl_Jour'), 1),
# (65, PyQt4.QtCore.QString(u'AppelNonConcl_Mois'), 1),
# (66, PyQt4.QtCore.QString(u'AppelNonConcl_Annee'), 1),
# (67, PyQt4.QtCore.QString(u'ServitudeCase'), 0),
# (68, PyQt4.QtCore.QString(u'PasClasseACase'), 0),
# (69, PyQt4.QtCore.QString(u'BranchementsCase'), 0),
# (70, PyQt4.QtCore.QString(u'Recommandations'), 1),
# (71, PyQt4.QtCore.QString(u'RubriquesGuide'), 1),
# (72, PyQt4.QtCore.QString(u''), 0),  # possible
# (73, PyQt4.QtCore.QString(u''), 0),  # pas possible
# (74, PyQt4.QtCore.QString(u'MesuresSecurite'), 1),
# (75, PyQt4.QtCore.QString(u'MesuresSecurite2'), 1),
# (76, PyQt4.QtCore.QString(u'DispositifsSecurite'), 2),
# (77, PyQt4.QtCore.QString(u'TelEndommagement'), 1),
# (78, PyQt4.QtCore.QString(u'Endommagement'), 1),
# (79, PyQt4.QtCore.QString(u'NomResponsableDossier'), 1),
# (80, PyQt4.QtCore.QString(u'D\xe9signationService'), 1),
# (81, PyQt4.QtCore.QString(u'TelResponsableDossier'), 1),
# (82, PyQt4.QtCore.QString(u'NomSignataire'), 1),
# (83, PyQt4.QtCore.QString(u'JourRecepisse'), 1),
# (84, PyQt4.QtCore.QString(u'MoisRecepisse'), 1),
# (85, PyQt4.QtCore.QString(u'AnneeRecepisse'), 1),
# (86, PyQt4.QtCore.QString(u'NbPJ'), 1)]


def findId(l, txt):
    id_f = -1
    for i, j in enumerate(l):
        if txt == j.name():
            id_f = i
            break
    return id_f


def saveChangePoppler(dlg):
    if POPPLER is False:
        return None, None
    line = [
        [dlg.Denomination,              3],
        [dlg.ComplementAdresse,         4],
        [dlg.NoVoie,                    5],
        [dlg.LieuditBP,                 6],
        [dlg.CodePostal,                7],
        [dlg.Commune,                   8],
        [dlg.Pays,                      9],
        [dlg.NoGu,                      10],
        [dlg.ReferenceExploitant,       11],
        [dlg.NoAffaireDeclarant,        12],
        [dlg.Personne_Contacter,        13],
        [dlg.CommuneTravaux,            17],
        [dlg.AdresseTravaux,            18],
        [dlg.RaisonSocialeExploitant,   19],
        [dlg.ContactExploitant,         20],
        [dlg.NoVoieExploitant,          21],
        [dlg.LieuditBPExploitant,       22],
        [dlg.CodePostalExploitant,      23],
        [dlg.CommuneExploitant,         24],
        [dlg.TelExploitant,             25],
        [dlg.FaxExploitant,             26],
        [dlg.InfoPreciser,              28],
        [dlg.DistanceReseau,            30],
        [dlg.ModifPrevue,               35],
        [dlg.RepresentantExploitant,    37],
        [dlg.TelModification,           38],
        [dlg.Ref1,                      40],
        [dlg.Ref2,                      48],
        [dlg.Echelle1,                  41],
        [dlg.Echelle2,                  49],
        [dlg.Profondeur1,               46],
        [dlg.Profondeur2,               54],
        [dlg.Materiau1,                 47],
        [dlg.Materiau2,                 55],
        [dlg.Recommandations,           70],
        [dlg.RubriquesGuide,            71],
        [dlg.MesuresSecurite2,          75],
        [dlg.MesuresSecurite,           74],
        [dlg.TelEndommagement,          77],
        [dlg.Endommagement,             78],
        [dlg.NomResponsableDossier,     79],
        [dlg.DesignationService,        80],
        [dlg.TelResponsableDossier,     81],
        [dlg.NomSignataire,             82],
        # [dlg.signSignataire,            u"Signature"],
        [dlg.NbPJ,                      86]
    ]

    path = os.path.dirname(__file__)
    formulaire = os.path.join(path, 'cerfa_14435-03.pdf')
    print(formulaire)

    doc = popplerqt5.Poppler.Document.load(formulaire)

    try:
        page = doc.page(0)
    except:
        return None, None

    fields = page.formFields()

    # Change contenu lignes
    for i in line:
        if i[0].isEnabled():
            fields[i[1]].setText(i[0].text())

    # Change contenu checkbox
    for i in dlg.findChildren(QCheckBox):
        id_f = findId(fields, i.objectName())
        if id_f != -1:
            if i.isChecked():
                fields[id_f].setState(True)

    # Change contenu radio
    for i in dlg.findChildren(QRadioButton):
        name = i.objectName()
        id_f = findId(fields, name)
        if id_f != -1:
            if i.isChecked():
                fields[id_f].setState(True)
        else:
            # impossible d'automatiser puisqu'il n'y a pas
            # de nom dans les champs du pdf
            if name == "Possible":
                if i.isChecked():
                    fields[72].setState(True)
            elif name == "Impossible":
                if i.isChecked():
                    fields[73].setState(True)

    # Change dateTime
    for i in dlg.findChildren(QDateTimeEdit):
        name = i.objectName()
        date_obj = i.date()
        time_obj = i.time()
        ok = True  # cas particulier des EditionsPlans
        if name == 'EditionPlan1' and len(dlg.Ref1.text()) == 0:
            ok = False
        if name == 'EditionPlan2' and (len(dlg.Ref1.text()) == 0 or
                                       len(dlg.Ref2.text()) == 0):
            ok = False

        if i.isEnabled() and ok:
            # Cas particulier de AppelNonConcl_ Jour Mois et Annee
            ext = "AppelNonConcl"
            if name.find(ext) >= 0:
                id_f = findId(fields, ext + "_" + "Jour")
                if id_f != -1:
                    fields[id_f].setText(str(date_obj.day()).rjust(2, '0'))
                id_f = findId(fields, ext + "_" + "Mois")
                if id_f != -1:
                    fields[id_f].setText(str(date_obj.month()).rjust(2, '0'))
                id_f = findId(fields, ext + "_" + "Annee")
                if id_f != -1:
                    fields[id_f].setText(str(date_obj.year()).rjust(4))
            else:
                id_f = findId(fields, "Jour" + name)
                if id_f != -1:
                    fields[id_f].setText(str(date_obj.day()).rjust(2, '0'))
                id_f = findId(fields, "Mois" + name)
                if id_f != -1:
                    fields[id_f].setText(str(date_obj.month()).rjust(2, '0'))

                id_f = findId(fields, "Annee" + name)
                if id_f != -1:
                    fields[id_f].setText(str(date_obj.year()).rjust(4))

                # cas particulier des années
                # Les champs EditionsPlan ne sont pas
                # identiques pour les années, ils se nomment :
                # AnneeEditionN au lieu de AnneeEditionPlanN
                # où N est le numéro...
                len_p = len('Plan')
                id_p = name.find('Plan')
                name_alt = name[:id_p]+name[id_p+len_p:]
                id_f = findId(fields, "Annee" + name_alt)
                if id_f != -1:
                    fields[id_f].setText(str(date_obj.year()).rjust(4))

                id_f = findId(fields, "Heure" + name)
                if id_f != -1:
                    fields[id_f].setText(str(time_obj.hour()).rjust(2, '0'))
                id_f = findId(fields, "Minute" + name)
                if id_f != -1:
                    fields[id_f].setText(str(time_obj.minute()).rjust(2, '0'))

    # Change Menu
    for i in dlg.findChildren(QComboBox):
        name = i.objectName()
        id_f = findId(fields, name)
        if id_f != -1:
            if i.isEnabled():
                fields[id_f].setCurrentChoices([i.currentIndex()])
            else:
                fields[id_f].setCurrentChoices([0])

    # A changer
    titre = dlg.ReferenceExploitant.text()

    # Sortie
    out_dir = QSettings().value("/DICT/configRep")
    if QDir(out_dir).exists() is False or out_dir is None:
        out_dir = str(QDir.homePath())

    out = os.path.join(out_dir, QSettings().value("/DICT/prefRecep", "") +
                       titre + QSettings().value("/DICT/sufRecep", "") +
                       ".pdf")

    pdf = doc.pdfConverter()
    pdf.setOutputFileName(out)
    pdf.setPDFOptions(popplerqt5.Poppler.PDFConverter.WithChanges)
    pdf.convert()

    return titre, out
