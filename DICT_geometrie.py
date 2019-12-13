#!/usr/bin/env python
# -*- coding:utf-8 -*-

from __future__ import absolute_import
from builtins import str
from builtins import object
from qgis.core import (QgsGeometry, QgsCoordinateTransform, QgsFeature,
                       QgsFillSymbol, QgsVectorLayer, QgsProject)
from qgis.utils import iface
from qgis.PyQt.QtCore import (QSizeF, QSettings, QDir, Qt)
from qgis.PyQt.QtPrintSupport import QPrinter
from qgis.PyQt.QtGui import QPainter
from qgis.PyQt.QtWidgets import QMessageBox
from .DICT_dialog_composer import DICTDialogComposer
from math import ceil, pow


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

    def __findScale(self, scale):
        scales = [200, 250, 500, 750, 1000, 1500, 2000]
        if scale in scales:
            ind = scales.index(scale)
            leng = len(scales)
            if ind+1 == leng:
                return scales[leng]+500
            else:
                return scales[ind+1]

        scale = int(ceil(scale))
        scales.append(scale)
        scales.sort()
        ind = scales.index(scale)
        leng = len(scales)
        if ind+1 == leng:
            born = str(scale)[0:2]
            puiss = pow(10, len(str(scale))-2)
            hi = (int(born[0]) + 1) * 10
            lo = (int(born[0]) * 10) + 5

            rlo = lo - int(born)
            if rlo < 0:
                return hi * puiss
            else:
                return lo * puiss
        else:
            return scales[ind+1]

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

        layerCRSSrsid = mem_layer.crs().srsid()
        mc = iface.mapCanvas()
        projectCRSSrsid = mc.mapSettings().destinationCrs().srsid()

        geomBB = self._geom
        if layerCRSSrsid != projectCRSSrsid:
            geomBB.transform(QgsCoordinateTransform(layerCRSSrsid,
                                                    projectCRSSrsid))
        self._geomBB = geomBB.boundingBox()
        mc.setExtent(self._geomBB)

    def geometriePDF(self, titre, taillePlan):
        # Afficher un assistant de saisie pour le choix du composeur
        dlgConfigComposers = DICTDialogComposer(taillePlan)
        dlgConfigComposers.show()
        result = dlgConfigComposers.exec_()

        idx_plan = []

        if result:
            idx_plan = dlgConfigComposers.listComposers.selectedItems()
            # id_plan = dlgConfigComposers.listComposers.currentRow()
        # Sortie du plan en PDF
        composers = iface.activeComposers()

        out = []
        if len(idx_plan) > 0:

            for r in idx_plan:
                id_plan = dlgConfigComposers.listComposers.row(r)
                c = composers[id_plan].composition()

                # À configurer
                c_map_lists = c.composerMapItems()
                if(len(c_map_lists) == 0):
                    return out
                else:
                    c_map = c_map_lists[0]

                if c_map:
                    c_map.zoomToExtent(self._geomBB)

                    # A faire correctement
                    s = c_map.scale()
                    scal = self.__findScale(s)
                    iface.mapCanvas().zoomScale(scal)
                    c_map.setNewScale(scal)
                    c_map.updateCachedImage()
                    c_map.renderModeUpdateCachedImage()

                    # Sortie
                    out_dir = QSettings().value("/DICT/configRep")
                    if QDir(out_dir).exists() is False or out_dir is None:
                        out_dir = str(QDir.homePath())

                    pdf = out_dir + "/" + \
                        QSettings().value("/DICT/prefPlan", u"") + titre + \
                        QSettings().value("/DICT/sufPlan", u"") + \
                        str(id_plan) + ".pdf"

                    c.exportAsPDF(pdf)
                    out.append(pdf)

        return out
