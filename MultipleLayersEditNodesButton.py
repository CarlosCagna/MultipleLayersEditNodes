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
import win32api, win32con
import time



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
    
        def click(x,y):
            win32api.SetCursorPos((x,y))
            win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,x,y,0,0)
            time.sleep(0.005)
            win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,x,y,0,0)     
            time.sleep(0.005)    
            win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,x,y,0,0)
            time.sleep(0.005)
            win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,x,y,0,0)     
            time.sleep(0.005)                
            
            print win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,x,y,0,0)  
                
            
        point = self.toLayerCoordinates(self.layer, e.pos())
        d = self.iface.mapCanvas().mapUnitsPerPixel()*4
        layer_select = 'NULL' 
        select_line = False
        select_polygon = False

        count = 0
        
        
        for layer in iface.legendInterface().layers():                
            if iface.legendInterface().isLayerVisible(layer) and layer.type()==0:
                
                if layer.geometryType()==2 and layer.featureCount()>=count:
                    count = layer.featureCount()
                    for feat in layer.getFeatures():
                        if feat.geometry() <> None: 
                            if feat.geometry().intersects(QgsRectangle ((point.x()-d), (point.y()-d), (point.x()+d), (point.y()+d))) and layer.name() =='Setor':
                                layer_select = layer 
                                select_polygon = True
                            elif feat.geometry().intersects(QgsRectangle ((point.x()-d), (point.y()-d), (point.x()+d), (point.y()+d))) and select_polygon ==False:
                                layer_select = layer 
                        
        for layer in iface.legendInterface().layers():            
            if iface.legendInterface().isLayerVisible(layer) and layer.type()==0:
                if layer.geometryType()==1: 
                    for feat in layer.getFeatures():
                        if feat.geometry() <> None:
                            if feat.geometry().intersects(QgsRectangle ((point.x()-d), (point.y()-d), (point.x()+d), (point.y()+d))) and select_line == False:
                                layer_select = layer 
                                select_line = True
                             
        for layer in iface.legendInterface().layers():            
            if iface.legendInterface().isLayerVisible(layer) and layer.type()==0:
                if layer.geometryType()==0: 
                    for feat in layer.getFeatures():
                        if feat.geometry() <> None:
                            if feat.geometry().intersects(QgsRectangle ((point.x()-d), (point.y()-d), (point.x()+d), (point.y()+d))):
                                layer_select = layer       
                            
                
        #layer.select(feat.id())
        layer_select.startEditing()
        iface.legendInterface().setCurrentLayer(layer_select)
        iface.actionNodeTool().trigger()            
                
        select_line = False
        x,y= win32api.GetCursorPos()    
        click(x,y)		
        
                        
    
    def deactivate(self):
        if self is not None:     
            QgsMapTool.deactivate(self)
        
    def activate(self):
        QgsMapTool.activate(self)
    