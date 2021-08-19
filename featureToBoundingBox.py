from PyQt5.QtGui import *

def featuresToBoundingBox(layer:QgsVectorLayer):
    for f in layer.getFeatures():
        f.setGeometry(QgsGeometry.fromWkt(f.geometry().boundingBox().asWktPolygon()))
        layer.updateFeature(f)

palm = QgsProject.instance().mapLayersByName('palm')[0]

if palm.isEditable() :
    for f in palm.getFeatures():
        featuresToBoundingBox(palm)
else :
    with edit(palm):
        featuresToBoundingBox(palm)


train = QgsProject.instance().mapLayersByName('train')[0]

if train.isEditable() :
    for f in train.getFeatures():
        featuresToBoundingBox(train)
else :
    with edit(train):
        featuresToBoundingBox(train)