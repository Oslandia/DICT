# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DICT_dialog_composer
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
from qgis.utils import iface

FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'DICT_dialog_composer.ui'))


class DICTDialogComposer(QtWidgets.QDialog, FORM_CLASS):
    def __init__(self, taillePlan, parent=None):
        """Constructor."""
        super(DICTDialogComposer, self).__init__(parent)
        # Set up the user interface from Designer.
        # After setupUI you can access any designer object by doing
        # self.<objectname>, and you can use autoconnect slots - see
        # http://qt-project.org/doc/qt-4.8/designer-using-a-ui-file.html
        # #widgets-and-dialogs-with-auto-connect
        self.setupUi(self)

        composers = iface.activeComposers()
        compositions = [i.composerWindow().windowTitle() for i in
                        iface.activeComposers()]
        self.listComposers.addItems(compositions)
        self.listComposers.setSelectionMode(
                QtWidgets.QAbstractItemView.ExtendedSelection)
        j = 0
        for i in compositions:
            if i.find(taillePlan) != -1:
                self.listComposers.setCurrentRow(j)
                # break
            j += 1
