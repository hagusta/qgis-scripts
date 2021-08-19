sys.path.insert(1, 'scripts/')

palm = QgsProject.instance().mapLayersByName('palm')[0]
train = QgsProject.instance().mapLayersByName('train')[0]
ras = QgsProject.instance().mapLayersByName('kolovai-partial-9')[0]

del trainDs
importlib.reload(TrainDatasets)
from TrainDatasets import trainDatasets
trainDs=trainDatasets(train.getFeatures(), palm.getFeatures(), ras)
trainDs.create()



trainDs=trainDatasets(train.getFeatures(), palm.getFeatures(), ras)


distance = QgsDistanceArea()
crs = QgsCoordinateReferenceSystem("EPSG:3857 WGS 84")

rasExt=ras.extent()
rasPntMax=[rasExt.xMaximum(),rasExt.yMaximum()]
rasPntMin=[rasExt.xMinimum(),rasExt.yMinimum()]
pxH,pxW=ras.height(),ras.width()

pixelSizeX = ras.rasterUnitsPerPixelX()
pixelSizeY = ras.rasterUnitsPerPixelY()


ds = gdal.Open('kolovai-partial-9.tif') 
xoffset, px_w, rot1, yoffset, px_h, rot2 = ds.GetGeoTransform()
posX = px_w * x + rot1 * y + xoffset
posY = rot2 * x + px_h * y + yoffset

import osgeo.gdal as gdal
ds=gdal.open('kolovai-partial-9.tif')
dt=ds.GetGeoTransform()
w=ds.RasterXSize
h=ds.RasterYSize
minX,maxY=dt[0],dt[3]
res=dt[1]

dim=440

gdal.Warp('kolovai.'+str(feature.id())+'.jpg','kolovai-partial-9.tif',outputBounds=(xmin,ymin,xmax,ymax),dstNodata=-9999,format="JPEG")

gdal.Warp(fileoutname,fileinput,outputBounds(xmin,ymin,xmax,ymax),dstNodata=-9999)
gdal.Warp('testtrain1.tif',ds,outputBounds=(),dstNodata=-9999)


xmin,ymin = t.geometry().boundingBox().xMinimum(), t.geometry().boundingBox().yMinimum()
xmax,ymax = t.geometry().boundingBox().xMaximum(), t.geometry().boundingBox().yMaximum()


startPoint=QgsPointXY(xmin,ymax)
endPoint=QgsPointXY(xmax,ymin)
clippedArea=QgsRectangle(startPoint,endPoint)

