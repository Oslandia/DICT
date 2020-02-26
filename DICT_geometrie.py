#!/usr/bin/env python
# -*- coding:utf-8 -*-

from qgis.core import *
from qgis.gui import *
from qgis.utils import iface
from PyQt5.QtCore import *
from PyQt5.QtGui import QPainter
from PyQt5.QtPrintSupport import QPrinter
from PyQt5.QtWidgets import QMessageBox
from .DICT_dialog_composer import DICTDialogComposer
from math import ceil, pow
import os


class DICT_geometrie(object):
    def __init__(self, xml, epsg_tag, gml_tag, gml_tag_alt):

        msgBox = QMessageBox()
        msgBox.setTextFormat(Qt.RichText)
        try:
            self._epsg = self.__findEPSG(xml, epsg_tag)
        except:
            msgBox.setText("Erreur d'analyse du code EPSG.")
            msgBox.exec_()
            return
        try:
            self._geom = self.__getGeom(xml, gml_tag, gml_tag_alt)
        except:
            msgBox.setText("Erreur d'analyse de la géométrie.")
            msgBox.exec_()
            return

    def __dictGeom2qgisGeom(self, geom):
        geom = geom.replace(' ', '*')
        geom = geom.replace(',', ' ')
        geom = geom.replace('*', ',')

        wkt = "POLYGON ((" + geom + "))"
        return QgsGeometry.fromWkt(wkt)

    def __dictAltGeom2qgisGeom(self, geom):
        s = ""
        count = 0
        for i in geom:
            if i == ' ':
                if count % 2 == 0:
                    s += ','
                else:
                    s += ' '
                count += 1
            else:
                s += i
        return self.__dictGeom2qgisGeom(s)

    def __findEPSG(self, xml, epsg_tag):
        epsg_xml = xml.getElementsByTagName(epsg_tag)
        att = epsg_xml[0].attributes['srsName']
        nValue = att.firstChild.nodeValue
        posEpsg = nValue.rfind(':') + 1

        return nValue[posEpsg:]

    def __getGeom(self, xml, gml_tag, gml_tag_alt):
        version = -1
        geom_txt = xml.getElementsByTagName(gml_tag)
        if(len(geom_txt) > 0):
            version = 1
        else:
            geom_txt = xml.getElementsByTagName(gml_tag_alt)
            if(len(geom_txt) > 0):
                version = 2

        g = geom_txt[0].firstChild.nodeValue
        if version == 1:
            geom = self.__dictGeom2qgisGeom(g)
        elif version == 2:
            geom = self.__dictAltGeom2qgisGeom(g)
        

        return geom

    def addGeometrie(self):
        vl = "Polygon?crs=epsg:" + self._epsg + "&index=yes"
        mem_layer = QgsVectorLayer(vl, "Emprise du chantier", "memory")
        pr = mem_layer.dataProvider()

        f = QgsFeature()

        f.setGeometry(self._geom)

        pr.addFeatures([f])
        mem_layer.commitChanges()
        mem_layer.updateExtents()
        prop = mem_layer.renderer().symbol().symbolLayers()[0].properties()
        prop['color'] = '255,0,0,20'
        mem_layer.renderer().setSymbol(QgsFillSymbol.createSimple(prop))
        QgsProject.instance().addMapLayer(mem_layer)

        layerCRSSrsid = mem_layer.crs().authid()
        mc = iface.mapCanvas()
        projectCRSSrsid = mc.mapSettings().destinationCrs().authid()

        geomBB = self._geom
        sourceCrs = QgsCoordinateReferenceSystem(layerCRSSrsid)
        destCrs = QgsCoordinateReferenceSystem(projectCRSSrsid)
        tr = QgsCoordinateTransform(sourceCrs, destCrs, QgsProject.instance())
        geomBB.transform(tr)
        self._geomBB = geomBB.boundingBox()
        mc.setExtent(self._geomBB)
        mc.zoomScale(mc.scale() * 2)
        

    def geometriePDF(self, titre, taillePlan):
        # Display layout list
        dlgConfigComposers = DICTDialogComposer(taillePlan)
        dlgConfigComposers.show()
        result = dlgConfigComposers.exec_()

        idx_plan = []

        if result:
            idx_plan = dlgConfigComposers.listComposers.selectedItems()
        # Sortie du plan en PDF
            manager = QgsProject.instance().layoutManager()

        out = []
        if len(idx_plan) > 0:

            id_plan = dlgConfigComposers.listComposers.row(idx_plan[0])
            layout_name = dlgConfigComposers.layout_listArray[id_plan]
            layout = manager.layoutByName(layout_name)

            # Retrieve the layout's map Item 
            mapItem = layout.itemById("carte_1")
            mapItem.zoomToExtent(iface.mapCanvas().extent())
            # Only mean to edit an existing item found so far is getting said item's ID
            # there's the layoutItems() method to get the list of items from a layout 
            # but as of now is exclusive to C++ plugins

            # Output
            out_dir = QSettings().value("/DICT/configRep")
            if QDir(out_dir).exists() is False or out_dir is None:
                out_dir = str(QDir.homePath())

            pdf = out_dir + "/" + \
                QSettings().value("/DICT/prefPlan", "") + titre + \
                QSettings().value("/DICT/sufPlan", "") + ".pdf"

            exported_layout = QgsLayoutExporter(layout)
            exported_layout.exportToPdf(pdf, QgsLayoutExporter.PdfExportSettings())
            out.append(pdf)

        return out
