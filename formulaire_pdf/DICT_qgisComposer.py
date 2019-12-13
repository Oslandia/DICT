# -*- coding: utf-8 -*-
"""
Created on Thu May 26 08:43:47 2016

@author: Loïc BARTOLETTI
"""

from builtins import str
import codecs
import os
import shutil
import tempfile
from qgis.core import QgsLayout
from qgis.utils import iface
from qgis.PyQt.QtXml import QDomDocument
from qgis.PyQt.QtWidgets import QDateTimeEdit, QRadioButton, QCheckBox, QComboBox
from qgis.PyQt.QtGui import QPainter
from qgis.PyQt.QtPrintSupport import QPrinter
from qgis.PyQt.QtCore import Qt, QSettings, QSizeF, QDir
from ..DICT_dialog_wizard import DICTDialogWizard


def saveChangeQGis(dlg):
    line = [
        [dlg.Denomination,              u"dest_Denomination"],
        [dlg.ComplementAdresse,         u"dest_ComplementAdresse"],
        [dlg.NoVoie,                    u"dest_NoVoie"],
        [dlg.LieuditBP,                 u"dest_LieuditBP"],
        [dlg.CodePostal,                u"dest_CodePostal"],
        [dlg.Commune,                   u"dest_Commune"],
        [dlg.Pays,                      u"dest_Pays"],
        [dlg.NoGU,                      u"NoGU"],
        [dlg.ReferenceExploitant,       u"ReferenceExploitant"],
        [dlg.NoAffaireDeclarant,        u"NoAffaireDeclarant"],
        [dlg.Personne_Contacter,        u"Personne_Contacter"],
        [dlg.CommuneTravaux,            u"CommuneTravaux"],
        [dlg.AdresseTravaux,            u"AdresseTravaux"],
        [dlg.RaisonSocialeExploitant,   u"RaisonSocialeExploitant"],
        [dlg.ContactExploitant,         u"ContactExploitant"],
        [dlg.NoVoieExploitant,          u"NoVoieExploitant"],
        [dlg.LieuditBPExploitant,       u"LieuditBPExploitant"],
        [dlg.CodePostalExploitant,      u"CodePostalExploitant"],
        [dlg.CommuneExploitant,         u"CommuneExploitant"],
        [dlg.TelExploitant,             u"TelExploitant"],
        [dlg.FaxExploitant,             u"FaxExploitant"],
        [dlg.InfoPreciser,              u"InfoPreciser"],
        [dlg.DistanceReseau,            u"DistanceReseau"],
        [dlg.ModifPrevue,               u"ModifPrevue"],
        [dlg.RepresentantExploitant,    u"RepresentantExploitant"],
        [dlg.TelModification,           u"TelModification"],
        [dlg.Ref1,                      u"Ref1"],
        [dlg.Ref2,                      u"Ref2"],
        [dlg.Echelle1,                  u"Echelle1"],
        [dlg.Echelle2,                  u"Echelle2"],
        [dlg.Profondeur1,               u"Profondeur1"],
        [dlg.Profondeur2,               u"Profondeur2"],
        [dlg.Materiau1,                 u"Materiau1"],
        [dlg.Materiau2,                 u"Materiau2"],
        [dlg.Recommandations,           u"Recommandations"],
        [dlg.RubriquesGuide,            u"RubriquesGuide"],
        [dlg.MesuresSecurite2,          u"MesuresSecurite2"],
        [dlg.MesuresSecurite,           u"MesuresSecurite"],
        [dlg.TelEndommagement,          u"TelEndommagement"],
        [dlg.Endommagement,             u"Endommagement"],
        [dlg.NomResponsableDossier,     u"NomResponsableDossier"],
        [dlg.DesignationService,        u"DesignationService"],
        [dlg.TelResponsableDossier,     u"TelResponsableDossier"],
        [dlg.NomSignataire,             u"NomSignataire"],
        [dlg.signSignataire,            u"Signature"],
        [dlg.NbPJ,                      u"NbPJ"]
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
            contenu = contenu.replace(i[1], u"")

    # Change contenu checkbox
    for i in dlg.findChildren(QCheckBox):
        name = i.objectName()
        if i.isChecked():
            contenu = contenu.replace(name, u"X")
        else:
            contenu = contenu.replace(name, u"")

    # Change contenu radio
    for i in dlg.findChildren(QRadioButton):
        name = i.objectName()
        if i.isChecked():
            contenu = contenu.replace(name, u"X")
        else:
            contenu = contenu.replace(name, u"")

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
            contenu = contenu.replace("Jour"+name, u"")
            contenu = contenu.replace("Mois"+name, u"")
            contenu = contenu.replace("Annee"+name, u"")
            contenu = contenu.replace("Heure"+name, u"")
            contenu = contenu.replace("Minute"+name, u"")

    # Change Menu
    for i in dlg.findChildren(QComboBox):
        name = i.objectName()
        if i.isEnabled():
            contenu = contenu.replace(name, i.currentText())
        else:
            contenu = contenu.replace(name, u"")

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
    myComposition = QgsLayout(myMapRenderer)
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

    out = os.path.join(out_dir, QSettings().value("/DICT/prefRecep", u"") +
                       titre + QSettings().value("/DICT/sufRecep", u"") +
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
