from osgeo import gdal,ogr
from qgis._core import QgsFeatureIterator, \
    QgsRasterLayer, \
    QgsVectorLayer, \
    QgsFeature, \
    QgsRectangle, \
    QgsGeometry, \
    QgsPointXY, \
    QgsProject

class trainDatasets:
    def __init__(self, areas:QgsFeatureIterator, \
        features: QgsFeatureIterator, \
        raster: QgsRasterLayer, \
        dimension=416, \
        path='data/', \
        filename='bbox'):
        self.features=list(iter(features))
        self.raster=raster
        self.areas=list(iter(areas))
        self.path=path
        self.filename=filename
        self.pixelSize=raster.rasterUnitsPerPixelX()
        self.dh=(dimension*self.pixelSize)/2
        self.dw=(dimension*self.pixelSize)/2
    
    def create(self):

        def getCentroid(feature:QgsFeature):
            cnt=feature.geometry().centroid()
            return [cnt.asPoint().x(),cnt.asPoint().y()]
        
        def featuresInRect(area:QgsRectangle, \
            features:list, \
            debug = False, \
            areaThreshold=.8):
            fs=[]
            if debug: 
                print(debug,list(features))
                for f in iter(features): 
                    print('f ',f) 
            for f in features:
                a=f.geometry().intersection( \
                QgsGeometry.fromRect(area))
                if debug: print('a ',a.area(),'f.geometry().area()',f.geometry().area()) 
                if a.area()/f.geometry().area() >= areaThreshold:
                    fs.append(f)
            return fs
    
        def createLabel(area:QgsRectangle, \
            feature:QgsFeature):
            bboxes=featuresInRect(area,self.features,debug=False)
            areaBox=[[area.xMinimum(),area.yMaximum()] ,\
                [area.xMaximum(),area.yMinimum()]]
            with open(self.path + 'labels/' + self.filename + '.'+ \
                str(feature.id()) +'.txt','w') as file:
                for box in bboxes:
                    #print(box.id(),'box')
                    bbox=box.geometry().boundingBox()
                    bboxPt=[[bbox.xMinimum(),bbox.yMaximum()],\
                        [bbox.xMaximum(),bbox.yMinimum()]]
                    fPixel=[[round(abs(bboxPt[0][0]-areaBox[0][0])/ \
                        self.pixelSize),round(abs(bboxPt[0][1]-areaBox[0][1] \
                        )/self.pixelSize)],[round(abs(bboxPt[1][0]- \
                        areaBox[0][0])/self.pixelSize), \
                        round(abs(bboxPt[1][1]-areaBox[0][1])/self.pixelSize)]]
                    file.write('0,'+ str(fPixel[0][0]) + ',' + \
                        str(fPixel[0][1]) + ',' + str(fPixel[1][0]) + \
                        ',' + str(fPixel[1][1]) + '\n')
                        
        def create(feature:QgsFeature):
            cX,cY=getCentroid(feature)
            xmin,ymin=cX-self.dw,cY-self.dh
            xmax,ymax=cX+self.dw,cY+self.dh
            startPoint=QgsPointXY(xmin,ymin)
            endPoint=QgsPointXY(xmax,ymax)
            clippedArea=QgsRectangle(startPoint,endPoint)
            resL=createLabel(clippedArea,feature)
            resI=gdal.Warp(
                self.path + 'images/'+self.filename +'.' \
                +str(feature.id()) \
                +'.jpg', self.raster.source(), \
                outputBounds=(xmin,ymin,xmax,ymax), \
                dstNodata=-9999, \
                format="JPEG")
            return resI,resL
        
        areas=[area.geometry().boundingBox() \
            for area in self.areas]
            
        #print('areas',areas,self.features)
        
        features=[ f for area in areas for f in featuresInRect(area=area,features=self.features) ]
            
        for feature in features:
            #print(feature.id())
            res=create(feature)
    



