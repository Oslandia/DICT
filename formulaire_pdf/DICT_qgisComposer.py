# -*- coding: utf-8 -*-
"""
Created on Thu May 26 08:43:47 2016

@author: Loïc BARTOLETTI
"""

import codecs
import os
import shutil
import tempfile
from qgis.core import *
from qgis.gui import *
from qgis.utils import iface
from PyQt5.QtXml import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from ..DICT_dialog_wizard import DICTDialogWizard


def saveChangeQGis(dlg):
    line = [
        [dlg.Denomination,              "dest_Denomination"],
        [dlg.ComplementAdresse,         "dest_ComplementAdresse"],
        [dlg.NoVoie,                    "dest_NoVoie"],
        [dlg.LieuditBP,                 "dest_LieuditBP"],
        [dlg.CodePostal,                "dest_CodePostal"],
        [dlg.Commune,                   "dest_Commune"],
        [dlg.Pays,                      "dest_Pays"],
        [dlg.NoGu,                      "NoGu"],
        [dlg.ReferenceExploitant,       "ReferenceExploitant"],
        [dlg.NoAffaireDeclarant,        "NoAffaireDeclarant"],
        [dlg.Personne_Contacter,        "Personne_Contacter"],
        [dlg.CommuneTravaux,            "CommuneTravaux"],
        [dlg.AdresseTravaux,            "AdresseTravaux"],
        [dlg.RaisonSocialeExploitant,   "RaisonSocialeExploitant"],
        [dlg.ContactExploitant,         "ContactExploitant"],
        [dlg.NoVoieExploitant,          "NoVoieExploitant"],
        [dlg.LieuditBPExploitant,       "LieuditBPExploitant"],
        [dlg.CodePostalExploitant,      "CodePostalExploitant"],
        [dlg.CommuneExploitant,         "CommuneExploitant"],
        [dlg.TelExploitant,             "TelExploitant"],
        [dlg.FaxExploitant,             "FaxExploitant"],
        [dlg.InfoPreciser,              "InfoPreciser"],
        [dlg.DistanceReseau,            "DistanceReseau"],
        [dlg.ModifPrevue,               "ModifPrevue"],
        [dlg.RepresentantExploitant,    "RepresentantExploitant"],
        [dlg.TelModification,           "TelModification"],
        [dlg.Ref1,                      "Ref1"],
        [dlg.Ref2,                      "Ref2"],
        [dlg.Echelle1,                  "Echelle1"],
        [dlg.Echelle2,                  "Echelle2"],
        [dlg.Profondeur1,               "Profondeur1"],
        [dlg.Profondeur2,               "Profondeur2"],
        [dlg.Materiau1,                 "Materiau1"],
        [dlg.Materiau2,                 "Materiau2"],
        [dlg.Recommandations,           "Recommandations"],
        [dlg.RubriquesGuide,            "RubriquesGuide"],
        [dlg.MesuresSecurite2,          "MesuresSecurite2"],
        [dlg.MesuresSecurite,           "MesuresSecurite"],
        [dlg.TelEndommagement,          "TelEndommagement"],
        [dlg.Endommagement,             "Endommagement"],
        [dlg.NomResponsableDossier,     "NomResponsableDossier"],
        [dlg.DesignationService,        "DesignationService"],
        [dlg.TelResponsableDossier,     "TelResponsableDossier"],
        [dlg.NomSignataire,             "NomSignataire"],
        [dlg.signSignataire,            "Signature"],
        [dlg.NbPJ,                      "NbPJ"]
    ]

    path = os.path.dirname(__file__)
    fdt, form = tempfile.mkstemp()
    formulaire = path + "/Formulaire_DICT.qpt"
    shutil.copy2(formulaire, form)
    fdn, newfile = tempfile.mkstemp()

    f = codecs.open(form, encoding="utf-8")
    n = codecs.open(newfile, "w", encoding="utf-8")

    contenu = f.read()

    # Image du CERFA
    contenu = contenu.replace("CHEMIN_VERS_IMAGE", path)

    # Change contenu lignes
    for i in line:
        if i[0].isEnabled():
            contenu = contenu.replace(i[1], Qt.escape(i[0].text()))
        else:
            contenu = contenu.replace(i[1], "")

    # Change contenu checkbox
    for i in dlg.findChildren(QCheckBox):
        name = i.objectName()
        if i.isChecked():
            contenu = contenu.replace(name, "X")
        else:
            contenu = contenu.replace(name, "")

    # Change contenu radio
    for i in dlg.findChildren(QRadioButton):
        name = i.objectName()
        if i.isChecked():
            contenu = contenu.replace(name, "X")
        else:
            contenu = contenu.replace(name, "")

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
            contenu = contenu.replace("Jour" + name,
                                      str(date_obj.day()).rjust(2, '0'))
            contenu = contenu.replace("Mois" + name,
                                      str(date_obj.month()).rjust(2, '0'))
            contenu = contenu.replace("Annee" + name,
                                      str(date_obj.year()).rjust(4))
            contenu = contenu.replace("Heure" + name,
                                      str(time_obj.hour()).rjust(2, '0'))
            contenu = contenu.replace("Minute" + name,
                                      str(time_obj.minute()).rjust(2, '0'))
        else:
            contenu = contenu.replace("Jour"+name, "")
            contenu = contenu.replace("Mois"+name, "")
            contenu = contenu.replace("Annee"+name, "")
            contenu = contenu.replace("Heure"+name, "")
            contenu = contenu.replace("Minute"+name, "")

    # Change Menu
    for i in dlg.findChildren(QComboBox):
        name = i.objectName()
        if i.isEnabled():
            contenu = contenu.replace(name, i.currentText())
        else:
            contenu = contenu.replace(name, "")

    n.write(contenu)

    n.close()
    f.close()

    shutil.copy2(newfile, form)

    # A changer
    titre = dlg.ReferenceExploitant.text()
    pdf = formulaireQGis(titre, form)

    os.close(fdt)
    os.remove(form)
    os.close(fdn)
    os.remove(newfile)

    return titre, pdf


def formulaireQGis(titre, path):
    myMapRenderer = iface.mapCanvas().mapSettings()
    # Load template from file
    myComposition = QgsComposition(myMapRenderer)
    myTemplateFile = file(path, 'rt')
    myTemplateContent = myTemplateFile.read()
    myTemplateFile.close()
    myDocument = QDomDocument()
    myDocument.setContent(myTemplateContent)
    myComposition.loadFromTemplate(myDocument)

    printer = QPrinter()
    printer.setOutputFormat(QPrinter.PdfFormat)

    # Sortie
    out_dir = QSettings().value("/DICT/configRep")
    if QDir(out_dir).exists() is False or out_dir is None:
        out_dir = str(QDir.homePath())

    out = os.path.join(out_dir, QSettings().value("/DICT/prefRecep", "") +
                       titre + QSettings().value("/DICT/sufRecep", "") +
                       ".pdf")

    printer.setOutputFileName(out)
    printer.setPaperSize(QSizeF(myComposition.paperWidth(),
                                myComposition.paperHeight()),
                         QPrinter.Millimeter)
    printer.setFullPage(True)
    printer.setColorMode(QPrinter.Color)
    printer.setResolution(myComposition.printResolution())

    pdfPainter = QPainter(printer)
    paperRectMM = printer.pageRect(QPrinter.Millimeter)
    paperRectPixel = printer.pageRect(QPrinter.DevicePixel)
    myComposition.render(pdfPainter, paperRectPixel, paperRectMM)
    pdfPainter.end()

    return out
