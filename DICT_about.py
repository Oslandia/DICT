
# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DICTAbout
                                 A QGIS plugin
 DICT
                             -------------------
        begin                : 2020-03-06
        git sha              : $Format:%H$
        copyright            : (C) 2020 by Loïc BARTOLETTI
        email                : loic.bartoletti@oslandia.com
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

FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'DICT_about.ui'), resource_suffix='')


class DICTAbout(QtWidgets.QDialog, FORM_CLASS):
    def __init__(self, parent=None):
        """Constructor."""
        super(DICTAbout, self).__init__(parent)
        self.setupUi(self)

        self.rejected.connect(self.onReject)
        self.buttonBox.rejected.connect(self.onReject)
        self.buttonBox.accepted.connect(self.onAccept)

    def onAccept(self):
        self.accept()

    def onReject(self):
        self.close()
