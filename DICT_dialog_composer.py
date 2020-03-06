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

from PyQt5 import uic, QtCore, QtWidgets
from qgis.utils import iface
from qgis.core import QgsLayoutManager, QgsProject

FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'DICT_dialog_composer.ui'))


class DICTDialogComposer(QtWidgets.QDialog, FORM_CLASS):
    def __init__(self, taillePlan, parent=None):
        """Constructor."""
        super(DICTDialogComposer, self).__init__(parent)

        self.setupUi(self)


        projectInstance = QgsProject.instance()
        manager = projectInstance.layoutManager()
        layouts_list = manager.printLayouts()
        layout_listArray = []

        for layout in layouts_list:
            layout_listArray.append(layout.name())
        self.layout_listArray = layout_listArray
        self.listComposers.addItems(layout_listArray)
        self.listComposers.setSelectionMode(
                QtWidgets.QAbstractItemView.ExtendedSelection)

        j = 0
        for i in layout_listArray:
            if i.find(taillePlan) != -1:
                self.listComposers.setCurrentRow(j)
                break
            j += 1
