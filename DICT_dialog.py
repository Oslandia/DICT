# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DICTDialog
                                 A QGIS plugin
 DICT
                             -------------------
        begin                : 2015-08-19
        git sha              : $Format:%H$
        copyright            : (C) 2015 by Loïc BARTOLETTI
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

from qgis.PyQt import QtWidgets, uic, QtCore

FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'DICT_dialog_base.ui'))


class DICTDialog(QtWidgets.QDialog, FORM_CLASS):
    def __init__(self, parent=None):
        """Constructor."""
        super(DICTDialog, self).__init__(parent)
        # Set up the user interface from Designer.
        # After setupUI you can access any designer object by doing
        # self.<objectname>, and you can use autoconnect slots - see
        # http://qt-project.org/doc/qt-4.8/designer-using-a-ui-file.html
        # #widgets-and-dialogs-with-auto-connect
        self.setupUi(self)

        self.toolButton.pressed.connect(self.showDialog)

    def showDialog(self):

        fname = QtWidgets.QFileDialog.getOpenFileName(
                self, 'Open file',
                QtCore.QSettings().value("/DICT/configRepXML",
                                         QtCore.QDir.homePath()),
                "fichier XML (*.xml *.XML)")

        if fname:
            f = open(fname, 'r')

            with f:
                self.lineEdit.setText(fname)
