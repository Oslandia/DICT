# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DICTDialogConfig
                                 A QGIS plugin
 DICT
                             -------------------
        begin                : 2015-08-19
        git sha              : $Format:%H$
        copyright            : (C) 2015 by Loïc BARTOLETTI + some random trainee in 2019 who adapted the whole code in Py3 for free
        email                : lbartoletti@tuxfamily.org
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""

import os

from PyQt5 import uic, QtCore, QtWidgets
from sys import platform as _platform

FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'DICT_dialog_config.ui'))


class DICTDialogConfig(QtWidgets.QDialog, FORM_CLASS):
    def __init__(self, parent=None):
        """Constructor."""
        super(DICTDialogConfig, self).__init__(parent)
        # Set up the user interface from Designer.
        # After setupUI you can access any designer object by doing
        # self.<objectname>, and you can use autoconnect slots - see
        # http://qt-project.org/doc/qt-4.8/designer-using-a-ui-file.html
        # #widgets-and-dialogs-with-auto-connect
        self.setupUi(self)

        self.configRep.setText(QtCore.QSettings().value(
                                "/DICT/configRep",
                                QtCore.QDir.homePath()))
        self.configRepXML.setText(QtCore.QSettings().value(
                                "/DICT/configRepXML",
                                QtCore.QDir.homePath()))
        self.configPDFTK.setText(QtCore.QSettings().value(
                                "/DICT/configPDFTK",
                                QtCore.QDir.homePath()))
        self.configExtension.setText(QtCore.QSettings().value(
                                "/DICT/configExtension"))
        self.signSignature.setText(QtCore.QSettings().value(
                                "/DICT/signSignature"))
        self.signNom.setText(QtCore.QSettings().value("/DICT/signNom"))
        self.respTel.setText(QtCore.QSettings().value("/DICT/respTel"))
        self.respService.setText(QtCore.QSettings().value("/DICT/respService"))
        self.respNom.setText(QtCore.QSettings().value("/DICT/respNom"))
        self.coordFax.setText(QtCore.QSettings().value("/DICT/coordFax"))
        self.coordTel.setText(QtCore.QSettings().value("/DICT/coordTel"))
        self.coordCommune.setText(QtCore.QSettings().value(
                                "/DICT/coordCommune"))
        self.coordCP.setText(QtCore.QSettings().value("/DICT/coordCP"))
        self.coordBP.setText(QtCore.QSettings().value("/DICT/coordBP"))
        self.coordNumVoie.setText(QtCore.QSettings().value(
                                "/DICT/coordNumVoie"))
        self.coordPersonne.setText(QtCore.QSettings().value(
                                "/DICT/coordPersonne"))
        self.coordDenom.setText(QtCore.QSettings().value("/DICT/coordDenom"))
        self.TelEndommagement.setText(QtCore.QSettings().value(
                                "/DICT/TelEndommagement"))

        self.prefRecep.setText(QtCore.QSettings().value("/DICT/prefRecep"))
        self.sufRecep.setText(QtCore.QSettings().value("/DICT/sufRecep"))
        self.prefPlan.setText(QtCore.QSettings().value("/DICT/prefPlan"))
        self.sufPlan.setText(QtCore.QSettings().value("/DICT/sufPlan"))
        self.Endommagement.setText(QtCore.QSettings().value(
                                "/DICT/Endommagement"))
        if QtCore.QSettings().value("/DICT/casDT"):
            self.casDT.setChecked(True)
        else:
            self.casDT.setChecked(False)

        if QtCore.QSettings().value("/DICT/fusionPDF"):
            self.fusionPDF.setChecked(True)
        else:
            self.fusionPDF.setChecked(False)

        if QtCore.QSettings().value("/DICT/formQGIS", True):
            self.radioQGisComposer.setChecked(True)
            QtCore.QSettings().setValue("/DICT/formPoppler",
                                        self.radioPoppler.isChecked())
        else:
            self.radioQGisComposer.setChecked(False)

        if QtCore.QSettings().value("/DICT/formPoppler"):
            try:
                import popplerqt5
                self.radioQGisComposer.setChecked(False)
                QtCore.QSettings().setValue("/DICT/formPoppler",
                                            self.radioQGisComposer.isChecked())
                self.radioPoppler.setChecked(True)
            except:
                self.radioQGisComposer.setChecked(True)
                QtCore.QSettings().setValue("/DICT/formPoppler",
                                            self.radioPoppler.isChecked())

        self.toolButton.pressed.connect(
            lambda: self.showDialogConfig(self.configRep))
        self.toolButtonXML.pressed.connect(
            lambda: self.showDialogConfig(self.configRepXML))
        self.toolButtonPDFTK.pressed.connect(
            lambda: self.showDialogConfig(self.configPDFTK, "Executable"))

        self.okButton = self.button_box.button(QtWidgets.QDialogButtonBox.Ok)
        self.okButton.clicked.connect(self.accept)

        self.cancelButton = self.button_box.button(
                                QtWidgets.QDialogButtonBox.Cancel)
        self.cancelButton.clicked.connect(self.close)

    def showDialogConfig(self, obj, flags="Directory"):
        if flags == "Directory":
            fname = QtWidgets.QFileDialog.getExistingDirectory(
                            self, "Choisissez un répertoire :")
        elif flags == "Executable":
            fname, _ = QtWidgets.QFileDialog.getOpenFileName(
                            self, "Choisissez l'exécutable :")
        else:
            return

        if fname:
            obj.setText(fname)

    def rep(self, repertoire, nom):
        rep = repertoire.text()
        if rep:
            if QtCore.QFileInfo(rep).exists():
                QtCore.QSettings().setValue("/DICT/"+nom, rep)
            else:
                if str(QtCore.QFileInfo(rep).path()) != '.':
                    QtCore.QSettings().setValue("/DICT/" + nom,
                                                QtCore.QFileInfo(rep).path())
                else:
                    QtCore.QSettings().setValue("/DICT/" + nom,
                                                QtCore.QDir.homePath())
        else:
            QtCore.QSettings().setValue("/DICT/" + nom, QtCore.QDir.homePath())
        repertoire.setText(QtCore.QSettings().value("/DICT/" + nom))

    def accept(self):
        self.rep(self.configRep, "configRep")
        self.rep(self.configRepXML, "configRepXML")
        self.rep(self.configPDFTK, "configPDFTK")

        QtCore.QSettings().setValue("/DICT/configExtension",
                                    self.configExtension.text())
        QtCore.QSettings().setValue("/DICT/signSignature",
                                    self.signSignature.text())
        QtCore.QSettings().setValue("/DICT/signNom", self.signNom.text())
        QtCore.QSettings().setValue("/DICT/respTel", self.respTel.text())
        QtCore.QSettings().setValue("/DICT/respService",
                                    self.respService.text())
        QtCore.QSettings().setValue("/DICT/respNom", self.respNom.text())
        QtCore.QSettings().setValue("/DICT/coordFax", self.coordFax.text())
        QtCore.QSettings().setValue("/DICT/coordTel", self.coordTel.text())
        QtCore.QSettings().setValue("/DICT/coordCommune",
                                    self.coordCommune.text())
        QtCore.QSettings().setValue("/DICT/coordCP", self.coordCP.text())
        QtCore.QSettings().setValue("/DICT/coordBP", self.coordBP.text())
        QtCore.QSettings().setValue("/DICT/coordNumVoie",
                                    self.coordNumVoie.text())
        QtCore.QSettings().setValue("/DICT/coordPersonne",
                                    self.coordPersonne.text())
        QtCore.QSettings().setValue("/DICT/coordDenom", self.coordDenom.text())
        QtCore.QSettings().setValue("/DICT/TelEndommagement",
                                    self.TelEndommagement.text())
        QtCore.QSettings().setValue("/DICT/Endommagement",
                                    self.Endommagement.text())
        QtCore.QSettings().setValue("/DICT/prefRecep", self.prefRecep.text())
        QtCore.QSettings().setValue("/DICT/sufRecep", self.sufRecep.text())
        QtCore.QSettings().setValue("/DICT/prefPlan", self.prefPlan.text())
        QtCore.QSettings().setValue("/DICT/sufPlan", self.sufPlan.text())
        QtCore.QSettings().setValue("/DICT/casDT", self.casDT.isChecked())

        QtCore.QSettings().setValue("/DICT/fusionPDF",
                                    self.fusionPDF.isChecked())

        if self.radioPoppler.isChecked():
            try:
                import popplerqt5
                QtCore.QSettings().setValue("/DICT/formPoppler", True)
                QtCore.QSettings().setValue("/DICT/formQGIS", False)
                self.radioPoppler.setChecked(True)
            except:
                txt = "Poppler n'a pas été détecté sur votre système.\n"
                txt += "Le composeur QGis sera utilisé par défaut.\n"

                QtWidgets.QMessageBox.warning(self,
                                          "Erreur de configuration poppler",
                                          txt)

                self.radioQGisComposer.setChecked(True)
                QtCore.QSettings().setValue("/DICT/formPoppler", False)
                QtCore.QSettings().setValue("/DICT/formQGIS", True)
        else:
            self.radioQGisComposer.setChecked(True)
            QtCore.QSettings().setValue("/DICT/formPoppler", False)
            QtCore.QSettings().setValue("/DICT/formQGIS", True)

        self.close()

        return QtWidgets.QDialog.Accepted
