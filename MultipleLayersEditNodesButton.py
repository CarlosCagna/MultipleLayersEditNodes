'''
Created on 12/10/2014

@author: ferrari
'''
from qgis.gui import *
from qgis.core import *
from PyQt4.Qt import *
from PyQt4.QtCore import Qt
from qgis.gui import QgsMapTool
from qgis.utils import iface
from PyQt4 import QtGui
from qgis.core import *
from qgis.gui  import QgsMessageBar
from PyQt4.QtCore import Qt, QSettings, QTranslator, qVersion, QCoreApplication, QFileInfo
from PyQt4.QtGui import QMessageBox, QAction, QIcon, QProgressBar
from PyQt4.QtSql import *


class MultipleLayersEditNodesButton(QgsMapTool):

    def __init__(self, iface, canvas, action):
        self.canvas = canvas
        self.iface = iface
        self.layer= iface.activeLayer()
        self.active = False
        
        QgsMapTool.__init__(self, self.canvas)
        self.setCursor(Qt.CrossCursor)
        self.setAction(action)
    
    def canvasPressEvent(self, e):
        point = self.toLayerCoordinates(self.layer, e.pos())
        d = self.iface.mapCanvas().mapUnitsPerPixel()*4
        layer_select = 'NULL' 
        for layer in iface.legendInterface().layers():            
            if iface.legendInterface().isLayerVisible(layer):
                if layer.geometryType()==2: 
                    for feat in layer.getFeatures():
                        if feat.geometry() <> None: 
                            if feat.geometry().intersects(QgsRectangle ((point.x()-d), (point.y()-d), (point.x()+d), (point.y()+d))):
                                layer.select(feat.id())
                                layer.startEditing()
                                iface.legendInterface().setCurrentLayer(layer)
                                iface.actionNodeTool().trigger()
                                layer_select = layer 
                        
        for layer in iface.legendInterface().layers():            
            if iface.legendInterface().isLayerVisible(layer):
                if layer.geometryType()==1: 
                    for feat in layer.getFeatures():
                        if feat.geometry().intersects(QgsRectangle ((point.x()-d), (point.y()-d), (point.x()+d), (point.y()+d))):
                            layer.select(feat.id())
                            layer.startEditing()
                            iface.legendInterface().setCurrentLayer(layer)
                            iface.actionNodeTool().trigger()
                            layer_select = layer 
                             
        for layer in iface.legendInterface().layers():            
            if iface.legendInterface().isLayerVisible(layer):
                if layer.geometryType()==0: 
                    for feat in layer.getFeatures():
                        if feat.geometry().intersects(QgsRectangle ((point.x()-d), (point.y()-d), (point.x()+d), (point.y()+d))):
                            layer.select(feat.id())
                            layer.startEditing()
                            iface.legendInterface().setCurrentLayer(layer)
                            iface.actionNodeTool().trigger()
                            layer_select = layer       
        for layer in iface.legendInterface().layers():            
            if layer <> layer_select:
                layer.removeSelection()                

                        
    
    def deactivate(self):
        if self is not None:
            QgsMapTool.deactivate(self)
        
    def activate(self):
        QgsMapTool.activate(self)
    